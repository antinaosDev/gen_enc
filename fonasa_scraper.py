import asyncio
import pandas as pd
import random
import time
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# Configuración
EXCEL_PATH = r"D:\PROYECTOS PROGRAMACIÓN\ANTIGRAVITY_PROJECTS\encuesta_riesgo\datos_demograficos_3.xlsx"
OUTPUT_PATH = r"D:\PROYECTOS PROGRAMACIÓN\ANTIGRAVITY_PROJECTS\encuesta_riesgo\resultados_fonasa_3.xlsx"
URL_LOGIN = "https://frontintegrado.fonasa.cl/FrontIntegradoLogin/#!/inicio"
USERNAME = "18581575-7"
PASSWORD = "Alan.front1"
CONCURRENCY_LIMIT = 7 # Cantidad de pestañas simultáneas (Seguro para evitar bloqueo)

async def close_modals_if_present(page):
    """Intenta cerrar modales presionando Escape."""
    try:
        await page.keyboard.press("Escape")
    except:
        pass

async def process_rut(sem, context, rut, extra_data_entry, target_url):
    """
    Procesa un RUT individual en una pestaña nueva.
    """
    async with sem:
        page = await context.new_page()
        resultados_rut = []
        try:
            # Navegar directamente a la vista de búsqueda
            await page.goto(target_url, timeout=60000)
            
            # Esperar a que el input esté listo
            search_input_xpath = "xpath=//*[@id='BusquedaRun']/div[1]/div/form/div/div[1]/input"
            try:
                await page.wait_for_selector(search_input_xpath, timeout=15000)
            except:
                # Si falla, intentar recargar una vez
                await page.reload()
                await page.wait_for_selector(search_input_xpath, timeout=15000)

            distrito = extra_data_entry.get("DISTRITO", "")
            sector = extra_data_entry.get("SECTOR", "")
            
            # Interactuar con el Input (Manejo de Modales)
            search_input = page.locator(search_input_xpath)
            try:
                # Intentar click limpio
                await search_input.click(timeout=3000)
                await search_input.fill(rut)
            except Exception as e:
                # Si falla (modal invisible, etc), presionar Escape y reintentar
                # print(f"[{rut}] Input bloqueado, intentando Escape...")
                await page.keyboard.press("Escape")
                await asyncio.sleep(0.5) 
                await search_input.click(timeout=5000)
                await search_input.fill(rut)

            # Click Buscar
            search_btn_xpath = "xpath=//*[@id='BusquedaRun']/div[1]/div/form/div/div[2]/button[1]"
            await page.locator(search_btn_xpath).click()
            
            # Esperar Sidebar (Signo de éxito)
            sidebar_btn = page.locator("xpath=//*[@id='sidebarInt']/a[4]").first
            
            # Dinámica de espera: Esperamos botón sidebar O mensaje de error O tabla vacía
            # Para simplificar, esperamos sidebar un tiempo razonable
            found_sidebar = False
            try:
                await sidebar_btn.wait_for(state="visible", timeout=10000)
                found_sidebar = True
            except:
                # Si no aparece sidebar, quizás el RUT no existe o no cargó
                pass

            if found_sidebar:
                # Click en Sidebar (Manejo de Modales)
                try:
                    await sidebar_btn.click(timeout=3000)
                except Exception as e:
                     # print(f"[{rut}] Sidebar bloqueado, intentando Escape...")
                     await page.keyboard.press("Escape")
                     await asyncio.sleep(0.5)
                     await sidebar_btn.click(timeout=5000)

                # Esperar y extraer tabla
                table_xpath = "xpath=//*[@id='BusquedaRun']/div[3]/div/gestion-percapita/div[2]/div/percapita-detalle-cargas/div/table"
                try:
                    await page.locator(table_xpath).wait_for(state="visible", timeout=8000)
                    
                    # Extraer HTML (rápido y offload a pandas)
                    table_html = await page.locator(table_xpath).evaluate("el => el.outerHTML")
                    
                    # Ejecutar pandas en hilo principal (es breve)
                    dfs = pd.read_html(table_html)
                    if dfs:
                        df_table = dfs[0]
                        records = df_table.to_dict('records')
                        for record in records:
                            entry = {
                                "RUT_CONSULTADO": rut,
                                "DISTRITO": distrito,
                                "SECTOR": sector,
                                "ESTADO": "Exitoso"
                            }
                            entry.update(record)
                            resultados_rut.append(entry)
                    else:
                         resultados_rut.append({"RUT_CONSULTADO": rut, "DISTRITO": distrito, "SECTOR": sector, "ESTADO": "Sin Datos (Tabla vacía)"})
                
                except Exception as e:
                     # A veces entra al sidebar pero no hay tabla (RUT sin cargas)
                     resultados_rut.append({"RUT_CONSULTADO": rut, "DISTRITO": distrito, "SECTOR": sector, "ESTADO": "Sin Datos/No Tabla Visible"})
            else:
                 resultados_rut.append({"RUT_CONSULTADO": rut, "DISTRITO": distrito, "SECTOR": sector, "ESTADO": "Sin Datos/No Sidebar (Posible RUT inválido)"})

            # print(f"[{rut}] OK")
            
        except Exception as e:
            print(f"[{rut}] Error: {str(e)[:100]}")
            resultados_rut.append({
                "RUT_CONSULTADO": rut, 
                "DISTRITO": extra_data_entry.get("DISTRITO", ""),
                "SECTOR": extra_data_entry.get("SECTOR", ""),
                "ESTADO": "Error de Proceso", 
                "ERROR_MSG": str(e)
            })
        finally:
            await page.close()
        
        return resultados_rut

async def main():
    print("--- INICIANDO SCRAPER OPTIMIZADO (ASYNC) ---")
    
    # 1. Leer Excel y preparar datos
    try:
        print(f"Leyendo Excel: {EXCEL_PATH}")
        df = pd.read_excel(EXCEL_PATH)
        if "RUT" not in df.columns:
            print("Error: Columna 'RUT' no encontrada.")
            return
        
        ruts = df["RUT"].astype(str).tolist()
        
        # Leer datos extra
        try:
            df_extra = pd.read_excel(EXCEL_PATH, sheet_name="Hoja2")
            df_extra.columns = [c.strip().upper() for c in df_extra.columns]
            if "RUT" in df_extra.columns:
                # Convertir RUT de extra a string para asegurar match
                df_extra["RUT"] = df_extra["RUT"].astype(str)
                extra_data = df_extra.set_index("RUT")[["DISTRITO", "SECTOR"]].to_dict('index')
            else:
                print("Advertencia: Hoja2 sin columna RUT.")
                extra_data = {}
        except:
            print("Advertencia: No se pudo leer Hoja2.")
            extra_data = {}
            
    except Exception as e:
        print(f"Error fatal leyendo archivo: {e}")
        return

    print(f"Total RUTs a procesar: {len(ruts)}")
    print(f"Concurrencia: {CONCURRENCY_LIMIT} pestañas simultáneas")

    async with async_playwright() as p:
        # 2. Iniciar Browser y Contexto Global
        try:
            browser = await p.chromium.launch(channel="msedge", headless=False)
        except:
             print("Edge no encontrado, usando Chrome estándar.")
             browser = await p.chromium.launch(headless=False)
             
        context = await browser.new_context()
        
        # 3. Login Centralizado
        page_login = await context.new_page()
        try:
            print("Iniciando Login...")
            await page_login.goto(URL_LOGIN)
            await page_login.locator("xpath=/html/body/ui-view/login/div[3]/div/div[1]/form/div/ul/li[2]").click()
            await page_login.locator("xpath=//*[@id='usernameExterno']").fill(USERNAME)
            await page_login.locator("xpath=//*[@id='passwordExterno']").fill(PASSWORD)
            await page_login.locator("xpath=//*[@id='tab2']/form/div/button").click()
            
            # Esperar a que cargue el dashboard inicial
            await page_login.wait_for_load_state("networkidle")
            
            # Refrescar la página para actualizar estado (Requerimiento original)
            print("Refrescando la página para evitar bloqueo de UI...")
            await page_login.reload()
            await page_login.wait_for_load_state("networkidle")
            await asyncio.sleep(3) # Breve pausa necesaria para que el DOM se estabilice
            
            # Navegar al módulo específico para obtener la URL final correcta
            print("Entrando al módulo de Gestión...")
            # Click en el cuadro/tile del menú principal
            await page_login.locator("xpath=/html/body/ui-view/root/main/div/inicio/body-inicio/div[2]/div/div/div/div").click()
            
            # Esperar a que cambie la URL o aparezca el input de búsqueda
            await page_login.wait_for_selector("xpath=//*[@id='BusquedaRun']/div[1]/div/form/div/div[1]/input", timeout=20000)
            
            # Capturar la URL destino para los workers
            TARGET_URL = page_login.url
            print(f"URL Objetivo capturada: {TARGET_URL}")
            
            await page_login.close() # Ya no necesitamos la pestaña de login, el contexto tiene la sesión
            
        except Exception as e:
            print(f"Error en Login: {e}")
            await browser.close()
            return

        # 4. Procesamiento Paralelo
        print("Iniciando workers...")
        sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
        resultados_totales = []
        
        tasks = []
        # Crear tareas
        for i, rut in enumerate(ruts):
            # Obtener data extra (match string)
            data_entry = extra_data.get(rut, {})
            
            task = asyncio.create_task(process_rut(sem, context, rut, data_entry, TARGET_URL))
            tasks.append(task)
        
        # Ejecutar y monitorear
        total_done = 0
        total_tasks = len(tasks)
        
        # Barra de progreso simple
        start_time = time.time()
        
        try:
            for future in asyncio.as_completed(tasks):
                res = await future
                resultados_totales.extend(res)
                total_done += 1
                
                if total_done % 5 == 0:
                    elapsed = time.time() - start_time
                    avg = elapsed / total_done
                    eta = (total_tasks - total_done) * (avg / CONCURRENCY_LIMIT) # Estimado burdo
                    print(f"Progreso: {total_done}/{total_tasks} | Resultados: {len(resultados_totales)} | T: {elapsed:.1f}s")

        except (KeyboardInterrupt, asyncio.CancelledError):
            print("\n\n--- DETENCIÓN DE EMERGENCIA ---")
            print("Guardando lo que se ha procesado hasta ahora...")

        finally:
            # 5. Guardar Resultados Finales
            print("Guardando archivo Excel final...")
            try:
                if resultados_totales:
                    df_res = pd.DataFrame(resultados_totales)
                    df_res.to_excel(OUTPUT_PATH, index=False)
                    print(f"¡TERMINADO! Archivo guardado en: {OUTPUT_PATH}")
                else:
                    print("No se obtuvieron resultados para guardar.")
            except Exception as e:
                print(f"Error guardando Excel: {e}")
                # Backup CSV por si acaso
                if resultados_totales:
                     pd.DataFrame(resultados_totales).to_csv("backup_resultados.csv", index=False)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
