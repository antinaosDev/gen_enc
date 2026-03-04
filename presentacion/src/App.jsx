import React, { useState } from 'react';
import {
  BookOpen, Users, Activity, Shield, Map, AlertTriangle,
  CheckCircle, Info, FileText, ChevronRight, Target, Layout, Database
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('inicio');

  const renderContent = () => {
    switch (activeTab) {
      case 'inicio': return <Inicio />;
      case 'roles': return <Roles />;
      case 'proceso': return <Proceso />;
      case 'riesgo': return <Riesgo />;
      case 'indicadores': return <Indicadores />;
      default: return <Inicio />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-800">
      {/* Sidebar de Navegación */}
      <aside className="w-72 bg-blue-900 text-white flex flex-col shadow-xl z-20">
        <div className="p-6 border-b border-blue-800">
          <div className="bg-white p-3 rounded-xl inline-block mb-4 shadow-sm">
            <BookOpen className="h-8 w-8 text-blue-900" />
          </div>
          <h1 className="text-xl font-bold leading-tight">Portal de Protocolos</h1>
          <p className="text-blue-300 text-sm mt-1">CESFAM Cholchol</p>
        </div>

        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          <p className="text-xs font-bold text-blue-400 uppercase tracking-wider mb-3 px-3">Menú Principal</p>

          <NavItem active={activeTab === 'inicio'} onClick={() => setActiveTab('inicio')} icon={<Info className="h-5 w-5" />} label="Introducción y Objetivos" />
          <NavItem active={activeTab === 'roles'} onClick={() => setActiveTab('roles')} icon={<Users className="h-5 w-5" />} label="Roles y Responsabilidades" />
          <NavItem active={activeTab === 'proceso'} onClick={() => setActiveTab('proceso')} icon={<Layout className="h-5 w-5" />} label="Paso a Paso del Registro" />
          <NavItem active={activeTab === 'riesgo'} onClick={() => setActiveTab('riesgo')} icon={<Activity className="h-5 w-5" />} label="Estratificación de Riesgo" />
          <NavItem active={activeTab === 'indicadores'} onClick={() => setActiveTab('indicadores')} icon={<Target className="h-5 w-5" />} label="Indicadores MAIS" />
        </nav>

        <div className="p-4 bg-blue-950 text-xs text-blue-300">
          <p>Versión Final Oficial</p>
          <p>Ley N° 20.584 - Confidencialidad</p>
        </div>
      </aside>

      {/* Área de Contenido Principal */}
      <main className="flex-1 overflow-y-auto bg-gray-50/50 relative">
        {/* Header superior decorativo */}
        <header className="bg-white border-b px-8 py-5 sticky top-0 z-10 shadow-sm flex justify-between items-center">
          <h2 className="text-xl font-bold text-gray-800">Protocolo de Registro Familiar y Estudio de Familia</h2>
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-bold">Vigencia Indefinida</span>
        </header>

        <div className="p-8 max-w-5xl mx-auto pb-20">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

// --- Componentes Auxiliares ---

function NavItem({ active, onClick, icon, label }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 text-left ${active
          ? 'bg-blue-600 text-white shadow-md'
          : 'text-blue-100 hover:bg-blue-800'
        }`}
    >
      {icon}
      <span className="font-medium text-sm">{label}</span>
      {active && <ChevronRight className="h-4 w-4 ml-auto opacity-70" />}
    </button>
  );
}

// --- Vistas de Contenido ---

function Inicio() {
  return (
    <div className="space-y-8 animate-fade-in">
      <div className="bg-gradient-to-r from-blue-800 to-blue-600 rounded-2xl p-8 text-white shadow-lg">
        <h1 className="text-3xl font-bold mb-4">Modelo de Atención Integral en Cholchol</h1>
        <p className="text-blue-100 leading-relaxed max-w-3xl">
          En el contexto específico de nuestra comuna, caracterizada por su <strong>alta ruralidad y pertinencia cultural mapuche</strong>, la transición hacia una gestión clínica moderna y estandarizada es un imperativo ético y normativo.
          Este portal explica el uso obligatorio de la nueva <strong>Plataforma Digital ENC Familiar</strong>, diseñada para subsanar brechas históricas y dar cumplimiento a la Estrategia ECICEP.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <div className="flex items-center space-x-3 mb-4">
            <Target className="h-6 w-6 text-blue-600" />
            <h3 className="text-xl font-bold text-gray-800">Objetivo General</h3>
          </div>
          <p className="text-gray-600 leading-relaxed">
            Estandarizar de manera obligatoria y auditable el proceso integral de registro, evaluación de riesgo biopsicosocial y diseño de planes de intervención familiar en el CESFAM Cholchol y sus Postas dependientes, mediante el uso exclusivo de la Plataforma ENC Familiar.
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <div className="flex items-center space-x-3 mb-4">
            <Shield className="h-6 w-6 text-blue-600" />
            <h3 className="text-xl font-bold text-gray-800">Marco Normativo</h3>
          </div>
          <ul className="space-y-3 text-gray-600">
            <li className="flex items-start"><CheckCircle className="h-5 w-5 text-green-500 mr-2 shrink-0 mt-0.5" /> <span>Orientaciones Técnicas del MINSAL para el MAIS.</span></li>
            <li className="flex items-start"><CheckCircle className="h-5 w-5 text-green-500 mr-2 shrink-0 mt-0.5" /> <span>Estrategia de Cuidado Integral Centrado en las Personas (ECICEP).</span></li>
            <li className="flex items-start"><CheckCircle className="h-5 w-5 text-green-500 mr-2 shrink-0 mt-0.5" /> <span>Ley N° 20.584 de Derechos y Deberes de los Pacientes (Confidencialidad).</span></li>
          </ul>
        </div>
      </div>

      <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-2xl">
        <h4 className="font-bold text-blue-900 mb-2">Alcance Obligatorio</h4>
        <p className="text-blue-800 text-sm">
          Este protocolo es de conocimiento y aplicación estrictamente obligatorio para la totalidad de la dotación (profesionales, técnicos y administrativos) de los Sectores Sol, Luna y Postas de Salud Rural (PSR).
        </p>
      </div>
    </div>
  );
}

function Roles() {
  const roles = [
    {
      title: "Profesionales y Técnicos Clínicos",
      subtitle: "(Equipos de Cabecera)",
      icon: <Activity className="h-6 w-6 text-indigo-500" />,
      responsibilities: [
        "Autenticarse en el sistema con credenciales personales e intransferibles.",
        "Aplicar la Ficha Familiar digital de manera completa en atenciones o terreno.",
        "Coconstruir y digitar el Plan Consensuado con la familia.",
        "Exportar el PDF Oficial (TEST-001) y adjuntarlo a la ficha clínica (SSASUR)."
      ]
    },
    {
      title: "Jefaturas de Sector y Coord. Postas",
      subtitle: "(Sector Sol / Luna / Rural)",
      icon: <Users className="h-6 w-6 text-blue-500" />,
      responsibilities: [
        "Garantizar Reuniones de Sector mensuales proyectando la plataforma para análisis de casos.",
        "Visar los Planes de Intervención Familiar generados por sus equipos.",
        "Monitorear que la sectorización informática coincida con la territorialidad."
      ]
    },
    {
      title: "Referente Local MAIS / Estadístico",
      subtitle: "Gestión de Datos",
      icon: <Database className="h-6 w-6 text-emerald-500" />,
      responsibilities: [
        "Extraer mensualmente el reporte automatizado REM-P7.",
        "Auditar los registros ('logs') para asegurar el uso correcto.",
        "Administrar perfiles de usuario y actualizar el Diagnóstico Comunitario."
      ]
    },
    {
      title: "Encargado de Calidad",
      subtitle: "Auditoría Interna",
      icon: <Shield className="h-6 w-6 text-amber-500" />,
      responsibilities: [
        "Realizar auditorías cruzadas mensuales (mínimo 5 fichas) cotejando la plataforma con SSASUR.",
        "Monitorizar el cumplimiento de los flujos.",
        "Elaborar informes trimestrales de brechas."
      ]
    }
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold text-gray-800">Roles y Responsabilidades</h2>
        <p className="text-gray-500 mt-2">La implementación exitosa requiere el compromiso coordinado de toda la red institucional.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {roles.map((role, idx) => (
          <div key={idx} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center space-x-4 mb-4">
              <div className="bg-gray-50 p-3 rounded-full">
                {role.icon}
              </div>
              <div>
                <h3 className="font-bold text-gray-800">{role.title}</h3>
                <p className="text-xs text-gray-500 font-medium">{role.subtitle}</p>
              </div>
            </div>
            <ul className="space-y-2">
              {role.responsibilities.map((resp, i) => (
                <li key={i} className="text-sm text-gray-600 flex items-start">
                  <span className="text-blue-500 mr-2 mt-0.5">•</span>
                  {resp}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

function Proceso() {
  const steps = [
    { num: 1, title: "Autenticación y Apertura", desc: "El funcionario ingresa con sus credenciales. Debe hacer clic en 'Nueva Ficha' para purgar la caché y evitar contaminación cruzada de datos." },
    { num: 2, title: "Identificación y Sectorización", desc: "Ingreso de apellidos del grupo familiar, dirección exacta (vital para georreferenciación rural) y asignación al Sector correspondiente (Sol, Luna o PSR)." },
    { num: 3, title: "Digitación del Grupo Familiar", desc: "Registro exhaustivo de integrantes. Es obligatorio marcar la casilla 'Resp' al informante principal (Caso Índice) para el Genograma." },
    { num: 4, title: "Valoración de Riesgo", desc: "Aplicación de la pauta de 42 ítems y registro de factores protectores. El cálculo algorítmico es automático y en tiempo real." },
    { num: 5, title: "Plan de Intervención Consensuado", desc: "Redacción de acuerdos con la familia: Objetivos, Actividad (ej. VDI), Responsable y Plazos definidos en la hoja de ruta." },
    { num: 6, title: "Validación y Guardado", desc: "Al guardar el estudio, la plataforma asigna un ID de Evaluación único e irrepetible y lo inyecta en la base de datos central." },
    { num: 7, title: "Extracción y Trazabilidad", desc: "Generación del PDF Oficial (TEST-001). Este archivo debe ser adjuntado obligatoriamente a la Ficha Clínica Electrónica en SSASUR." }
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold text-gray-800">Procedimiento Operativo (Paso a Paso)</h2>
        <p className="text-gray-500 mt-2">Flujo obligatorio para atenciones en box, policlínico, ECICEP o trabajo en terreno (VDI).</p>
      </div>

      <div className="relative border-l-2 border-blue-200 ml-4 space-y-8 py-4">
        {steps.map((step) => (
          <div key={step.num} className="relative pl-8">
            {/* Círculo del número */}
            <div className="absolute -left-4 top-0 bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold shadow-md border-4 border-gray-50">
              {step.num}
            </div>

            <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="text-lg font-bold text-blue-900 mb-2">{step.title}</h3>
              <p className="text-gray-600 text-sm leading-relaxed">{step.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Riesgo() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold text-gray-800">Estratificación de Riesgo y Acciones Clínicas</h2>
        <p className="text-gray-500 mt-2">La plataforma calcula el nivel de riesgo en base a determinantes biológicos, ambientales y socioeconómicos, dictando la acción clínica a seguir.</p>
      </div>

      <div className="space-y-4">
        {/* Riesgo Leve */}
        <div className="flex bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="w-4 bg-green-500 shrink-0"></div>
          <div className="p-6 flex-1">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-xl font-bold text-gray-800">Riesgo Leve</h3>
              <span className="bg-green-100 text-green-800 font-bold px-3 py-1 rounded-full text-sm">0 - 14 puntos</span>
            </div>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Acción:</strong> Intervención preventiva en box.</div>
              <div className="bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Seguimiento:</strong> Reevaluación en 2 años o ante crisis.</div>
              <div className="md:col-span-2 bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Estrategia:</strong> Entrega de Guías Anticipatorias, consejería familiar breve y promoción del autocuidado.</div>
            </div>
          </div>
        </div>

        {/* Riesgo Moderado */}
        <div className="flex bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="w-4 bg-yellow-400 shrink-0"></div>
          <div className="p-6 flex-1">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-xl font-bold text-gray-800">Riesgo Moderado</h3>
              <span className="bg-yellow-100 text-yellow-800 font-bold px-3 py-1 rounded-full text-sm">15 - 29 puntos</span>
            </div>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Acción:</strong> Escalada a Visita Domiciliaria Integral (VDI).</div>
              <div className="bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Requisito Legal:</strong> Firma de Consentimiento Informado.</div>
              <div className="md:col-span-2 bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Estrategia:</strong> Planificación con equipo interdisciplinario y aplicación de instrumentos en terreno.</div>
            </div>
          </div>
        </div>

        {/* Riesgo Severo */}
        <div className="flex bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="w-4 bg-red-600 shrink-0"></div>
          <div className="p-6 flex-1">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-xl font-bold text-gray-800">Riesgo Severo / Alto</h3>
              <span className="bg-red-100 text-red-800 font-bold px-3 py-1 rounded-full text-sm">30+ puntos o Excepción</span>
            </div>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Acción:</strong> VDI prioritaria y Gestión de Caso (ECICEP G3).</div>
              <div className="bg-gray-50 p-3 rounded-lg"><strong className="text-gray-700">Estrategia:</strong> Análisis inmediato en Reunión de Sector.</div>
            </div>
            <div className="mt-4 bg-red-50 p-4 rounded-lg border border-red-100 text-sm">
              <div className="flex items-center font-bold text-red-800 mb-1"><AlertTriangle className="h-4 w-4 mr-2" /> REGLA DE EXCEPCIÓN CLÍNICA</div>
              <p className="text-red-700">La detección de <strong>Violencia Intrafamiliar (VIF)</strong> o <strong>Consumo problemático de sustancias</strong> fuerza automáticamente la clasificación a Riesgo Severo, ignorando el puntaje matemático.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Indicadores() {
  const kpis = [
    { ind: "Ind. 4.1", title: "Agrupación Familiar", type: "OBLIGATORIO", goal: ">30% Familias", desc: "Porcentaje de familias inscritas que se encuentran correctamente agrupadas y trazadas digitalmente en el sistema." },
    { ind: "Ind. 4.2", title: "Riesgo Familiar", type: "AUDITABLE", goal: ">30% Familias", desc: "Familias con instrumento de riesgo aplicado y vigente (antigüedad no mayor a 2 años en el sistema)." },
    { ind: "Ind. 4.3", title: "Visita Domiciliaria Integral (VDI)", type: "AUDITABLE", goal: "100% Cumplimiento", desc: "Pautas de cotejo de fichas clínicas que evidencien pauta VDI, acuerdos y seguimiento (PDF de Plataforma adjunto)." },
    { ind: "Ind. 5.1", title: "Planes de Cuidado Consensuados", type: "OBLIGATORIO", goal: "Auditoría de Pares", desc: "Garantizar que el plan de intervención ECICEP no sea exclusivamente biomédico, sino negociado con la familia y registrado." }
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold text-gray-800">Indicadores de Gestión y Calidad (MAIS 2026)</h2>
        <p className="text-gray-500 mt-2">El cumplimiento estricto de este protocolo impacta directamente en la Certificación MAIS y el consolidado estadístico REM-P7.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {kpis.map((kpi, idx) => (
          <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex justify-between items-start mb-4">
              <div>
                <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">{kpi.ind}</span>
                <h3 className="text-lg font-bold text-gray-800 mt-2">{kpi.title}</h3>
              </div>
              <span className={`text-xs font-bold px-2 py-1 rounded-full ${kpi.type === 'OBLIGATORIO' ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-600'}`}>
                {kpi.type}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-4 h-16">{kpi.desc}</p>
            <div className="border-t pt-4">
              <span className="text-sm text-gray-500 font-medium">Meta Institucional: </span>
              <span className="text-sm font-bold text-gray-800">{kpi.goal}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-blue-900 p-6 rounded-2xl text-white mt-8 flex items-center shadow-lg">
        <FileText className="h-10 w-10 text-blue-300 mr-4 shrink-0" />
        <div>
          <h4 className="font-bold text-lg">Reporte REM-P7</h4>
          <p className="text-blue-100 text-sm mt-1">La Plataforma ENC Familiar automatiza la extracción de datos para el REM-P7, eliminando el subregistro y las planillas manuales en el CESFAM y las Postas.</p>
        </div>
      </div>
    </div>
  );
}
