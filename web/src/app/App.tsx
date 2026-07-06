import { useState } from "react";
import {
  LayoutDashboard,
  CheckSquare,
  Bot,
  BookOpen,
  Radio,
  Database,
  ScrollText,
  Settings,
  Search,
  Bell,
  ArrowRight,
  CheckCircle,
  AlertTriangle,
  FileText,
  Book,
  Send,
  Plus,
  Download,
  RefreshCw,
  MessageSquare,
  Activity,
  ChevronRight,
  Shield,
  Zap,
} from "lucide-react";

// ─── Types ────────────────────────────────────────────────────────────────────
type Page =
  | "dashboard"
  | "tasks"
  | "agents"
  | "agent-detail"
  | "book-agent"
  | "gateway"
  | "queue"
  | "logs"
  | "settings";

type AgentStatus = "대기중" | "실행중" | "완료" | "실패";
type TaskStatus = "진행중" | "완료" | "마감 임박" | "검토 필요" | "등록 대기";
type Priority = "높음" | "중간" | "낮음";

// ─── Mock Data ────────────────────────────────────────────────────────────────
const mockTasks = [
  { id: 1, name: "ALD 분석 보고서 초안 작성", assignee: "김연구", due: "2025-07-07 15:00", priority: "높음" as Priority, status: "진행중" as TaskStatus, channel: "Telegram", agent: "document_agent" },
  { id: 2, name: "주간 업무 보고서 정리", assignee: "이담당", due: "2025-07-08 18:00", priority: "중간" as Priority, status: "완료" as TaskStatus, channel: "Telegram", agent: "document_agent" },
  { id: 3, name: "내일 오전 팀 회의 일정 등록", assignee: "박일정", due: "2025-07-07 09:00", priority: "높음" as Priority, status: "마감 임박" as TaskStatus, channel: "Telegram", agent: "schedule_agent" },
  { id: 4, name: "Q2 매출 데이터 CSV 분석", assignee: "최데이터", due: "2025-07-10 12:00", priority: "중간" as Priority, status: "진행중" as TaskStatus, channel: "Telegram", agent: "data_agent" },
  { id: 5, name: "ADK 기술문서 목차 생성", assignee: "정기술", due: "2025-07-12 17:00", priority: "낮음" as Priority, status: "등록 대기" as TaskStatus, channel: "Telegram", agent: "book_agent" },
  { id: 6, name: "반응형 웹 개발 업무 등록", assignee: "한개발", due: "2025-07-09 10:00", priority: "높음" as Priority, status: "검토 필요" as TaskStatus, channel: "Telegram", agent: "task_agent" },
];

const agents = [
  { id: "root_agent", name: "Root Agent", role: "사용자 요청 분석 및 sub_agent 위임 조율", status: "실행중" as AgentStatus, lastRequest: "ALD 보고서 요청 분석 및 라우팅", avgTime: "0.8s", tools: 0, isRoot: true },
  { id: "task_agent", name: "task_agent", role: "업무 등록, 조회, 상태 변경, 우선순위 관리", status: "대기중" as AgentStatus, lastRequest: "반응형 웹 개발 업무 등록", avgTime: "1.2s", tools: 4, isRoot: false },
  { id: "schedule_agent", name: "schedule_agent", role: "일정 등록, 회의 관리, 리마인드 설정", status: "완료" as AgentStatus, lastRequest: "팀 회의 리마인드 생성 (3건)", avgTime: "0.9s", tools: 5, isRoot: false },
  { id: "document_agent", name: "document_agent", role: "보고서, 회의록, 업무 문서 작성 및 정리", status: "실행중" as AgentStatus, lastRequest: "ALD 분석 보고서 초안 작성 중", avgTime: "3.4s", tools: 6, isRoot: false },
  { id: "data_agent", name: "data_agent", role: "엑셀/CSV 분석, 데이터 요약, 전처리", status: "완료" as AgentStatus, lastRequest: "Q2 매출 CSV 분석 완료 (1,248행)", avgTime: "2.1s", tools: 5, isRoot: false },
  { id: "book_agent", name: "book_agent", role: "기술문서, 교재, 보고서형 문서 구조 생성", status: "실패" as AgentStatus, lastRequest: "ADK 기술문서 목차 생성 (타임아웃)", avgTime: "4.7s", tools: 4, isRoot: false },
];

const allLogs = [
  { time: "14:23:11", layer: "Transfer", event: "sub_agent 위임 완료", agent: "document_agent", status: "완료", detail: "report_draft_tool 호출" },
  { time: "14:22:58", layer: "Root Agent", event: "업무 요청 분석 완료", agent: "root_agent", status: "완료", detail: "document_agent로 라우팅" },
  { time: "14:22:45", layer: "Runner", event: "세션 생성 완료", agent: "ADK Runner", status: "완료", detail: "session_id: usr_001" },
  { time: "14:22:30", layer: "Gateway", event: "Telegram 메시지 수신", agent: "TelegramAdapter", status: "완료", detail: "chat_id: 834920" },
  { time: "14:20:05", layer: "Tool Call", event: "schedule_reminder_tool 실행", agent: "schedule_agent", status: "완료", detail: "리마인드 3건 생성" },
  { time: "14:18:33", layer: "Tool Call", event: "csv_analysis_tool 실행", agent: "data_agent", status: "완료", detail: "rows: 1,248 / cols: 12" },
  { time: "14:15:22", layer: "Error", event: "book_agent 연결 타임아웃", agent: "book_agent", status: "실패", detail: "retry: 2/3" },
  { time: "14:12:01", layer: "Transfer", event: "task_agent 위임", agent: "task_agent", status: "완료", detail: "업무 3건 등록" },
  { time: "14:10:15", layer: "Gateway", event: "Telegram 메시지 수신", agent: "TelegramAdapter", status: "완료", detail: "chat_id: 839021" },
  { time: "14:09:55", layer: "Runner", event: "세션 재사용", agent: "ADK Runner", status: "완료", detail: "session_id: usr_001 (재사용)" },
  { time: "14:08:30", layer: "Root Agent", event: "멀티태스킹 요청 분해", agent: "root_agent", status: "완료", detail: "3개 sub_agent 병렬 위임" },
  { time: "14:05:12", layer: "Error", event: "data_agent 메모리 초과", agent: "data_agent", status: "실패", detail: "파일 크기 128MB 초과" },
];

// ─── Shared Components ────────────────────────────────────────────────────────
function StatusBadge({ status }: { status: string }) {
  const map: Record<string, { pill: string; dot: string }> = {
    실행중: { pill: "bg-blue-50 text-blue-700 border-blue-200", dot: "bg-blue-500" },
    완료:   { pill: "bg-green-50 text-green-700 border-green-200", dot: "bg-green-500" },
    대기중: { pill: "bg-gray-100 text-gray-500 border-gray-200", dot: "bg-gray-400" },
    실패:   { pill: "bg-red-50 text-red-700 border-red-200", dot: "bg-red-500" },
    "마감 임박": { pill: "bg-amber-50 text-amber-700 border-amber-200", dot: "bg-amber-500" },
    진행중: { pill: "bg-blue-50 text-blue-700 border-blue-200", dot: "bg-blue-500" },
    "등록 대기": { pill: "bg-gray-100 text-gray-500 border-gray-200", dot: "bg-gray-400" },
    "검토 필요": { pill: "bg-red-50 text-red-700 border-red-200", dot: "bg-red-500" },
    활성: { pill: "bg-green-50 text-green-700 border-green-200", dot: "bg-green-500" },
    보류: { pill: "bg-amber-50 text-amber-700 border-amber-200", dot: "bg-amber-500" },
    스캐폴드: { pill: "bg-purple-50 text-purple-700 border-purple-200", dot: "bg-purple-500" },
    미연동: { pill: "bg-gray-100 text-gray-500 border-gray-200", dot: "bg-gray-400" },
    "실행 가능": { pill: "bg-green-50 text-green-700 border-green-200", dot: "bg-green-500" },
  };
  const s = map[status] ?? { pill: "bg-gray-100 text-gray-500 border-gray-200", dot: "bg-gray-400" };
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${s.pill}`}>
      <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${s.dot}`} />
      {status}
    </span>
  );
}

function PriorityBadge({ priority }: { priority: Priority }) {
  const map: Record<Priority, string> = {
    높음: "text-red-600 bg-red-50 border border-red-100",
    중간: "text-amber-600 bg-amber-50 border border-amber-100",
    낮음: "text-gray-500 bg-gray-100 border border-gray-200",
  };
  return (
    <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${map[priority]}`}>{priority}</span>
  );
}

function ToggleSwitch({ value, onChange }: { value: boolean; onChange: () => void }) {
  return (
    <button
      onClick={onChange}
      className={`w-10 h-5 rounded-full transition-colors relative flex-shrink-0 ${value ? "bg-blue-600" : "bg-gray-200"}`}
    >
      <span className={`absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform ${value ? "translate-x-5" : "translate-x-0"}`} />
    </button>
  );
}

// ─── Sidebar ──────────────────────────────────────────────────────────────────
const navItems = [
  { id: "dashboard", label: "대시보드", icon: LayoutDashboard },
  { id: "tasks", label: "업무 관리", icon: CheckSquare },
  { id: "agents", label: "에이전트", icon: Bot },
  { id: "book-agent", label: "Book Agent", icon: BookOpen },
  { id: "gateway", label: "Gateway", icon: Radio },
  { id: "queue", label: "Queue & Heartbeat", icon: Database },
  { id: "logs", label: "시스템 로그", icon: ScrollText },
  { id: "settings", label: "설정", icon: Settings },
] as const;

function Sidebar({ page, setPage }: { page: Page; setPage: (p: Page) => void }) {
  return (
    <aside className="fixed left-0 top-0 h-full w-60 flex flex-col z-20" style={{ background: "#0C1B3A" }}>
      <div className="px-5 py-5 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-blue-500 flex items-center justify-center flex-shrink-0">
            <Zap size={17} className="text-white" />
          </div>
          <div>
            <div className="text-white font-bold text-sm leading-tight">KETI WorkOS</div>
            <div className="text-blue-300 text-xs mt-0.5">ADK 자동화 플랫폼</div>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        <div className="px-3 mb-2 text-blue-400 text-xs font-semibold uppercase tracking-wider">메뉴</div>
        {navItems.map(({ id, label, icon: Icon }) => {
          const active = page === id || (page === "agent-detail" && id === "agents");
          return (
            <button
              key={id}
              onClick={() => setPage(id as Page)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all font-medium ${
                active
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-blue-200 hover:bg-white/10 hover:text-white"
              }`}
            >
              <Icon size={15} />
              <span className="truncate">{label}</span>
            </button>
          );
        })}
      </nav>

      <div className="px-4 py-4 border-t border-white/10 space-y-2">
        <div className="text-xs text-blue-400 font-semibold mb-2">시스템 상태</div>
        {[
          { label: "Telegram", status: "활성", color: "bg-green-400", pulse: true },
          { label: "ADK Runner", status: "실행중", color: "bg-blue-400", pulse: false },
          { label: "Redis Queue", status: "스캐폴드", color: "bg-amber-400", pulse: false },
        ].map((s) => (
          <div key={s.label} className="flex items-center justify-between text-xs">
            <span className="text-blue-200">{s.label}</span>
            <div className="flex items-center gap-1.5">
              <span className={`w-1.5 h-1.5 rounded-full ${s.color} ${s.pulse ? "animate-pulse" : ""}`} />
              <span className={s.status === "활성" || s.status === "실행중" ? "text-green-400" : "text-amber-400"}>
                {s.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}

// ─── Header ───────────────────────────────────────────────────────────────────
const pageTitles: Record<Page, string> = {
  dashboard: "대시보드",
  tasks: "업무 관리",
  agents: "에이전트 현황",
  "agent-detail": "document_agent — 상세 정보",
  "book-agent": "Book Agent",
  gateway: "Gateway 채널 관리",
  queue: "Queue & Heartbeat",
  logs: "시스템 로그",
  settings: "설정",
};

function Header({ page }: { page: Page }) {
  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center px-6 gap-4 z-10">
      <div className="flex-1">
        <h1 className="text-sm font-semibold text-gray-800">{pageTitles[page]}</h1>
      </div>
      <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 w-72">
        <Search size={13} className="text-gray-400 flex-shrink-0" />
        <input
          className="flex-1 text-xs bg-transparent outline-none text-gray-600 placeholder-gray-400"
          placeholder="업무, 에이전트, 로그 검색..."
        />
      </div>
      <div className="flex items-center gap-2">
        <button className="relative w-9 h-9 flex items-center justify-center rounded-xl hover:bg-gray-100 transition-colors">
          <Bell size={16} className="text-gray-500" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border border-white" />
        </button>
        <div className="w-9 h-9 rounded-xl bg-[#1B3A6B] flex items-center justify-center text-white text-xs font-bold">
          KW
        </div>
      </div>
    </header>
  );
}

// ─── Dashboard Page ───────────────────────────────────────────────────────────
function DashboardPage({ setPage }: { setPage: (p: Page) => void }) {
  const stats = [
    { label: "오늘의 업무", value: "12", sub: "+3 신규 등록", icon: CheckSquare, bg: "bg-blue-500" },
    { label: "마감 임박", value: "3", sub: "24시간 이내", icon: AlertTriangle, bg: "bg-amber-500" },
    { label: "실행 중인 Agent", value: "2", sub: "document, data", icon: Bot, bg: "bg-indigo-500" },
    { label: "완료된 작업", value: "47", sub: "이번 주 누적", icon: CheckCircle, bg: "bg-green-500" },
    { label: "실패/검토 필요", value: "2", sub: "조치 필요", icon: AlertTriangle, bg: "bg-red-500" },
    { label: "Telegram 수신", value: "156", sub: "오늘 메시지", icon: MessageSquare, bg: "bg-purple-500" },
  ];

  const flowSteps = [
    { label: "Telegram", sub: "메시지 수신", bg: "bg-blue-50 border-blue-200", text: "text-blue-700", dot: "bg-blue-500" },
    { label: "ADK Runner", sub: "세션 관리", bg: "bg-indigo-50 border-indigo-200", text: "text-indigo-700", dot: "bg-indigo-500" },
    { label: "Root Agent", sub: "요청 분석", bg: "bg-violet-50 border-violet-200", text: "text-violet-700", dot: "bg-violet-500" },
    { label: "Sub Agent", sub: "업무 위임", bg: "bg-purple-50 border-purple-200", text: "text-purple-700", dot: "bg-purple-500" },
    { label: "Tool 실행", sub: "도구 호출", bg: "bg-pink-50 border-pink-200", text: "text-pink-700", dot: "bg-pink-500" },
    { label: "최종 응답", sub: "결과 전송", bg: "bg-green-50 border-green-200", text: "text-green-700", dot: "bg-green-500" },
  ];

  const recentActivities = [
    { agent: "task_agent", event: "업무 등록 완료 — 반응형 웹 개발 업무", time: "방금 전", status: "완료" },
    { agent: "document_agent", event: "보고서 초안 생성 — ALD 분석 보고서", time: "3분 전", status: "완료" },
    { agent: "schedule_agent", event: "회의 리마인드 생성 — 팀 스탠드업", time: "7분 전", status: "완료" },
    { agent: "data_agent", event: "CSV 분석 완료 — Q2 매출 데이터 1,248행", time: "12분 전", status: "완료" },
    { agent: "book_agent", event: "목차 생성 실패 — ADK 기술문서 (타임아웃)", time: "15분 전", status: "실패" },
  ];

  return (
    <div className="p-6 space-y-5">
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="bg-white rounded-2xl border border-gray-100 p-4 shadow-sm hover:shadow-md transition-shadow">
            <div className={`w-9 h-9 rounded-xl ${s.bg} flex items-center justify-center mb-3`}>
              <s.icon size={16} className="text-white" />
            </div>
            <div className="text-2xl font-bold text-gray-900 leading-none">{s.value}</div>
            <div className="text-xs font-semibold text-gray-700 mt-1.5">{s.label}</div>
            <div className="text-xs text-gray-400 mt-0.5">{s.sub}</div>
          </div>
        ))}
      </div>

      {/* Routing Flow */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="flex items-center justify-between mb-5">
          <div>
            <div className="text-sm font-semibold text-gray-800">Agent 라우팅 흐름</div>
            <div className="text-xs text-gray-400 mt-1">Telegram → ADK Runner → Root Agent → Sub Agent → Tool → 최종 응답</div>
          </div>
          <div className="flex items-center gap-2 text-xs text-green-600 bg-green-50 border border-green-200 px-3 py-1.5 rounded-full font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
            실시간 실행 중
          </div>
        </div>

        <div className="flex items-center gap-2 overflow-x-auto pb-2">
          {flowSteps.map((step, i) => (
            <div key={step.label} className="flex items-center gap-2 flex-shrink-0">
              <div className={`border rounded-2xl px-4 py-3 ${step.bg} min-w-[108px]`}>
                <div className="flex items-center gap-1.5 mb-1">
                  <span className={`w-2 h-2 rounded-full ${step.dot}`} />
                  <span className={`text-xs font-semibold ${step.text}`}>{step.label}</span>
                </div>
                <div className={`text-xs opacity-60 ${step.text}`}>{step.sub}</div>
              </div>
              {i < flowSteps.length - 1 && (
                <ArrowRight size={13} className="text-gray-300 flex-shrink-0" />
              )}
            </div>
          ))}
        </div>

        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="text-xs text-gray-400 mb-2.5">Root Agent → Sub Agent 위임 구조</div>
          <div className="flex items-center gap-2 flex-wrap">
            <div className="bg-violet-100 border border-violet-200 text-violet-700 text-xs px-3 py-1.5 rounded-xl font-semibold">
              Root Agent
            </div>
            <ChevronRight size={12} className="text-gray-300" />
            {["task_agent", "schedule_agent", "document_agent", "data_agent", "book_agent"].map((a) => (
              <button
                key={a}
                onClick={() => setPage("agent-detail")}
                className="bg-gray-50 border border-gray-200 rounded-xl px-3 py-1.5 text-xs text-gray-600 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-700 transition-all font-mono"
              >
                {a}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-gray-700">Telegram 채널 활성</span>
            <StatusBadge status="활성" />
          </div>
          <div className="text-xs text-gray-500 leading-relaxed">Long polling으로 메시지 수신 중. ADK Runner로 전달 활성화.</div>
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-gray-700">Redis Queue</span>
            <StatusBadge status="스캐폴드" />
          </div>
          <div className="text-xs text-gray-500 leading-relaxed">분산락 및 작업 큐 미연동. 연동 준비 완료 대기 중.</div>
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-gray-700">Heartbeat</span>
            <StatusBadge status="미연동" />
          </div>
          <div className="text-xs text-gray-500 leading-relaxed">Cron 기반 능동 트리거 준비 중. 변경 감지 엔진 미연동.</div>
        </div>
      </div>

      {/* Recent Logs */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-100">
          <div className="text-sm font-semibold text-gray-800">최근 Agent 실행 로그</div>
          <button onClick={() => setPage("logs")} className="text-xs text-blue-600 hover:text-blue-700 font-medium">
            전체 보기 →
          </button>
        </div>
        <div className="divide-y divide-gray-50">
          {recentActivities.map((a, i) => (
            <div key={i} className="flex items-center gap-4 px-5 py-3 hover:bg-gray-50/50 transition-colors">
              <span className="text-xs font-mono text-gray-400 w-16 flex-shrink-0">{a.time}</span>
              <span className="text-xs font-mono font-semibold text-blue-600 w-28 flex-shrink-0">{a.agent}</span>
              <span className="flex-1 text-xs text-gray-600">{a.event}</span>
              <StatusBadge status={a.status} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Tasks Page ───────────────────────────────────────────────────────────────
function TasksPage() {
  const [filter, setFilter] = useState("전체");
  const [input, setInput] = useState("");
  const [extracted, setExtracted] = useState(false);
  const filters = ["전체", "진행중", "완료", "마감 임박", "검토 필요"];
  const filtered = filter === "전체" ? mockTasks : mockTasks.filter((t) => t.status === filter);

  const handleSend = () => { if (input.trim()) setExtracted(true); };

  return (
    <div className="p-6 space-y-5">
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="text-sm font-semibold text-gray-800 mb-3">채팅형 업무 입력</div>
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder='예: "내일 오후 3시까지 ALD 분석 보고서 초안 작성해줘"'
            className="flex-1 text-sm border border-gray-200 rounded-xl px-4 py-2.5 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all"
          />
          <button
            onClick={handleSend}
            className="flex items-center gap-2 bg-blue-600 text-white text-sm px-4 py-2.5 rounded-xl hover:bg-blue-700 transition-colors font-medium"
          >
            <Send size={14} />
            분석
          </button>
        </div>

        {extracted && (
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-2xl">
            <div className="text-xs font-semibold text-blue-700 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500" />
              자동 추출 결과 — Root Agent 분석 완료
            </div>
            <div className="grid grid-cols-3 gap-2.5">
              {[
                ["업무명", "ALD 분석 보고서 초안 작성"],
                ["마감일", "내일 오후 3시 (2025-07-07 15:00)"],
                ["담당 Agent", "document_agent"],
                ["우선순위", "높음"],
                ["상태", "등록 대기"],
                ["감지 채널", "Web 직접 입력"],
              ].map(([k, v]) => (
                <div key={k} className="bg-white rounded-xl px-3 py-2.5 border border-blue-100">
                  <div className="text-xs text-gray-400">{k}</div>
                  <div className="text-xs font-semibold text-gray-800 mt-0.5">{v}</div>
                </div>
              ))}
            </div>
            <div className="flex gap-2 mt-3">
              <button className="bg-blue-600 text-white text-xs px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                업무 등록
              </button>
              <button onClick={() => setExtracted(false)} className="text-gray-600 text-xs px-4 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                취소
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-gray-100">
          <div className="flex gap-1">
            {filters.map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`text-xs px-3 py-1.5 rounded-lg transition-colors font-medium ${
                  filter === f ? "bg-blue-600 text-white" : "text-gray-500 hover:bg-gray-100"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
          <button className="flex items-center gap-1.5 text-xs bg-blue-600 text-white px-3 py-1.5 rounded-lg hover:bg-blue-700 transition-colors font-medium">
            <Plus size={12} />
            업무 등록
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-gray-100 bg-gray-50">
                {["업무명", "담당자", "마감일", "우선순위", "상태", "생성 채널", "담당 Agent"].map((h) => (
                  <th key={h} className="text-left px-4 py-3 text-gray-500 font-semibold whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {filtered.map((t) => (
                <tr key={t.id} className="hover:bg-gray-50/60 transition-colors">
                  <td className="px-4 py-3 font-medium text-gray-800 max-w-[190px] truncate">{t.name}</td>
                  <td className="px-4 py-3 text-gray-600">{t.assignee}</td>
                  <td className="px-4 py-3 text-gray-500 font-mono whitespace-nowrap">{t.due}</td>
                  <td className="px-4 py-3"><PriorityBadge priority={t.priority} /></td>
                  <td className="px-4 py-3"><StatusBadge status={t.status} /></td>
                  <td className="px-4 py-3 text-gray-500">{t.channel}</td>
                  <td className="px-4 py-3">
                    <span className="font-mono text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md text-xs">{t.agent}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ─── Agents Page ──────────────────────────────────────────────────────────────
function AgentsPage({ setPage }: { setPage: (p: Page) => void }) {
  const subAgents = agents.filter((a) => !a.isRoot);
  const root = agents.find((a) => a.isRoot)!;

  return (
    <div className="p-6 space-y-5">
      <div className="bg-gradient-to-br from-[#0C1B3A] to-[#1E3A6E] rounded-2xl p-5 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-white/15 flex items-center justify-center">
              <Shield size={22} className="text-blue-300" />
            </div>
            <div>
              <div className="font-bold text-lg">Root Agent</div>
              <div className="text-blue-200 text-sm mt-0.5">{root.role}</div>
            </div>
          </div>
          <div className="text-right">
            <StatusBadge status={root.status} />
            <div className="text-xs text-blue-300 mt-2">평균 응답 {root.avgTime}</div>
          </div>
        </div>
        <div className="mt-5 pt-4 border-t border-white/10">
          <div className="text-xs text-blue-300 mb-2.5">최근 처리: {root.lastRequest}</div>
          <div className="flex gap-2 flex-wrap">
            {subAgents.map((a) => (
              <button
                key={a.id}
                onClick={() => setPage("agent-detail")}
                className="bg-white/10 hover:bg-white/20 text-blue-100 text-xs px-3 py-1.5 rounded-xl transition-colors font-mono"
              >
                {a.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 xl:grid-cols-3 gap-4">
        {subAgents.map((a) => (
          <button
            key={a.id}
            onClick={() => setPage("agent-detail")}
            className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 text-left hover:border-blue-200 hover:shadow-md transition-all group cursor-pointer"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-blue-50 flex items-center justify-center">
                  <Bot size={15} className="text-blue-600" />
                </div>
                <span className="font-mono text-sm font-bold text-gray-800">{a.name}</span>
              </div>
              <StatusBadge status={a.status} />
            </div>
            <div className="text-xs text-gray-500 mb-3 leading-relaxed">{a.role}</div>
            <div className="border-t border-gray-100 pt-3 grid grid-cols-2 gap-3">
              <div>
                <div className="text-xs text-gray-400">최근 처리</div>
                <div className="text-xs text-gray-700 mt-0.5 line-clamp-2 leading-snug">{a.lastRequest}</div>
              </div>
              <div>
                <div className="text-xs text-gray-400">평균 응답</div>
                <div className="text-xs font-mono font-bold text-gray-700 mt-0.5">{a.avgTime}</div>
                <div className="text-xs text-gray-400 mt-1">Tools {a.tools}개</div>
              </div>
            </div>
            <div className="mt-3 text-xs text-blue-500 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
              상세 보기 →
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

// ─── Agent Detail Page ────────────────────────────────────────────────────────
function AgentDetailPage({ setPage }: { setPage: (p: Page) => void }) {
  const tools = [
    { name: "report_draft_tool", desc: "보고서 초안 작성", status: "활성" },
    { name: "meeting_notes_tool", desc: "회의록 정리", status: "활성" },
    { name: "memo_format_tool", desc: "업무 메모 정리", status: "활성" },
    { name: "doc_summary_tool", desc: "문서 요약", status: "활성" },
    { name: "template_tool", desc: "문서 템플릿 적용", status: "대기중" },
    { name: "export_pdf_tool", desc: "PDF 내보내기", status: "대기중" },
  ];
  const execLogs = [
    { time: "14:22:30", event: "root_agent received user request", type: "info" },
    { time: "14:22:35", event: "transfer_to_agent(document_agent)", type: "transfer" },
    { time: "14:22:36", event: "document_agent 활성화, 요청 수신 완료", type: "info" },
    { time: "14:22:38", event: "document_agent selected report_draft_tool", type: "tool" },
    { time: "14:22:40", event: "report_draft_tool 실행 중... (2,847 토큰 생성)", type: "tool" },
    { time: "14:23:11", event: "final_response generated — 보고서 초안 완성", type: "success" },
  ];
  const typeStyle: Record<string, string> = {
    info: "text-blue-600 bg-blue-50 border-blue-100",
    transfer: "text-violet-600 bg-violet-50 border-violet-100",
    tool: "text-amber-600 bg-amber-50 border-amber-100",
    success: "text-green-600 bg-green-50 border-green-100",
  };

  return (
    <div className="p-6 space-y-5">
      <button onClick={() => setPage("agents")} className="text-xs text-gray-400 hover:text-gray-600 flex items-center gap-1 font-medium">
        ← 에이전트 목록으로
      </button>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="flex items-center gap-4">
          <div className="w-13 h-13 w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center flex-shrink-0">
            <FileText size={22} className="text-blue-600" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-3">
              <h2 className="font-bold text-gray-900 text-lg font-mono">document_agent</h2>
              <StatusBadge status="실행중" />
            </div>
            <div className="text-sm text-gray-500 mt-0.5">보고서, 회의록, 업무 문서 작성 전문 에이전트</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-400">평균 응답 시간</div>
            <div className="font-mono text-2xl font-bold text-gray-800 mt-0.5">3.4s</div>
            <div className="text-xs text-gray-400 mt-0.5">Tools 6개 연결</div>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="text-xs font-semibold text-gray-600 mb-2">SOUL 역할 정의</div>
          <div className="bg-gray-50 rounded-xl px-4 py-3 text-xs text-gray-600 leading-relaxed border border-gray-100">
            당신은 KETI WorkOS의 문서 작성 전문가입니다. 사용자의 요청을 분석하여 보고서 초안, 회의록, 업무 메모를 정확하고 구조적으로 작성합니다. 항상 한국어로 응답하며, 문서의 목적과 독자를 고려한 적절한 형식을 선택합니다.
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-5">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <div className="text-sm font-semibold text-gray-800 mb-3">연결 Tools ({tools.length}개)</div>
          <div className="space-y-2">
            {tools.map((t) => (
              <div key={t.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                <div>
                  <div className="font-mono text-xs font-semibold text-gray-700">{t.name}</div>
                  <div className="text-xs text-gray-400 mt-0.5">{t.desc}</div>
                </div>
                <StatusBadge status={t.status} />
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <div className="text-sm font-semibold text-gray-800 mb-3">Tool 호출 로그 (최근 세션)</div>
          <div className="space-y-2.5">
            {execLogs.map((l, i) => (
              <div key={i} className="flex gap-2.5 text-xs">
                <span className="font-mono text-gray-400 w-14 flex-shrink-0 pt-0.5">{l.time}</span>
                <span className={`px-2 py-0.5 rounded-md text-xs font-medium border flex-shrink-0 h-fit ${typeStyle[l.type]}`}>
                  {l.type}
                </span>
                <span className="text-gray-600 leading-relaxed">{l.event}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-5">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <div className="text-sm font-semibold text-gray-800 mb-3">입력 프롬프트</div>
          <div className="bg-gray-50 rounded-xl p-4 text-xs text-gray-700 font-mono leading-relaxed border border-gray-100">
            "내일 오후 3시까지 ALD 분석 보고서 초안 작성해줘. 분석 결과는 첨부 파일 참고해서 요약 섹션, 주요 발견사항, 결론 순으로 구성해줘."
          </div>
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <div className="flex items-center justify-between mb-3">
            <div className="text-sm font-semibold text-gray-800">Agent 응답</div>
            <StatusBadge status="완료" />
          </div>
          <div className="bg-blue-50 rounded-xl p-4 text-xs text-gray-700 leading-relaxed border border-blue-100">
            ALD 분석 보고서 초안을 작성했습니다.<br /><br />
            <strong className="text-gray-800">1. 요약</strong><br />
            ALD 공정 분석 결과, 박막 두께 균일성 98.3% 달성...<br /><br />
            <strong className="text-gray-800">2. 주요 발견사항</strong><br />
            온도 분포 최적화 필요 구간 확인됨...<br /><br />
            <strong className="text-gray-800">3. 결론</strong><br />
            현재 공정 파라미터 조정 권장...
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Book Agent Page ──────────────────────────────────────────────────────────
function BookAgentPage() {
  const [docType, setDocType] = useState("guidebook");
  const [step, setStep] = useState(0);
  const [title, setTitle] = useState("Google ADK 멀티에이전트 개발 가이드");
  const [audience, setAudience] = useState("AI 시스템 개발자, MLOps 엔지니어");
  const [goal, setGoal] = useState("ADK 기반 멀티에이전트 아키텍처 설계 및 구현 능력 향상");

  const docTypes = [
    { id: "textbook", label: "교재", icon: "📚" },
    { id: "guidebook", label: "가이드북", icon: "📖" },
    { id: "report", label: "보고서", icon: "📋" },
    { id: "story", label: "스토리", icon: "📝" },
    { id: "general", label: "일반 문서", icon: "📄" },
  ];
  const steps = ["기획", "목차 생성", "챕터 작성", "검토", "수정", "Export"];
  const mockToc = [
    { ch: 1, title: "Google ADK 소개 및 아키텍처 이해", pages: 15 },
    { ch: 2, title: "멀티에이전트 설계 패턴", pages: 22 },
    { ch: 3, title: "Root Agent와 Sub Agent 구현", pages: 31 },
    { ch: 4, title: "Tool 연동 및 Function Calling", pages: 18 },
    { ch: 5, title: "세션 관리와 ADK Runner", pages: 14 },
    { ch: 6, title: "채널 Gateway 연동 (Telegram, Slack)", pages: 20 },
    { ch: 7, title: "운영 환경 배포 및 모니터링", pages: 16 },
    { ch: 8, title: "실전 프로젝트: KETI WorkOS 구축", pages: 25 },
  ];

  return (
    <div className="p-6 space-y-5">
      <div className="grid grid-cols-3 gap-5">
        <div className="col-span-2 space-y-4">
          {/* Steps */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
            <div className="text-sm font-semibold text-gray-800 mb-4">진행 단계</div>
            <div className="flex items-center">
              {steps.map((s, i) => (
                <div key={s} className="flex items-center flex-1 min-w-0">
                  <div className="flex flex-col items-center flex-shrink-0">
                    <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                      i < step ? "bg-green-500 text-white" : i === step ? "bg-blue-600 text-white ring-4 ring-blue-100" : "bg-gray-100 text-gray-400"
                    }`}>
                      {i < step ? "✓" : i + 1}
                    </div>
                    <div className={`text-xs mt-1.5 whitespace-nowrap ${i === step ? "text-blue-600 font-semibold" : i < step ? "text-green-600" : "text-gray-400"}`}>
                      {s}
                    </div>
                  </div>
                  {i < steps.length - 1 && (
                    <div className={`flex-1 h-0.5 mx-1 mb-5 ${i < step ? "bg-green-400" : "bg-gray-200"}`} />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Doc Type */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
            <div className="text-sm font-semibold text-gray-800 mb-3">문서 유형 선택</div>
            <div className="flex gap-2 flex-wrap">
              {docTypes.map((d) => (
                <button
                  key={d.id}
                  onClick={() => setDocType(d.id)}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm transition-all font-medium ${
                    docType === d.id
                      ? "border-blue-400 bg-blue-50 text-blue-700"
                      : "border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50"
                  }`}
                >
                  <span>{d.icon}</span>
                  {d.label}
                </button>
              ))}
            </div>
          </div>

          {/* Inputs */}
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 space-y-4">
            <div className="text-sm font-semibold text-gray-800">문서 정보 입력</div>
            {[
              { label: "문서 제목", value: title, set: setTitle, ph: "예: ADK 개발 가이드" },
              { label: "대상 독자", value: audience, set: setAudience, ph: "예: AI 개발자, 엔지니어" },
              { label: "문서 목표", value: goal, set: setGoal, ph: "예: ADK 기반 시스템 구현 능력 향상" },
            ].map(({ label, value, set, ph }) => (
              <div key={label}>
                <label className="text-xs font-semibold text-gray-600 block mb-1.5">{label}</label>
                <input
                  value={value}
                  onChange={(e) => set(e.target.value)}
                  placeholder={ph}
                  className="w-full text-sm border border-gray-200 rounded-xl px-3.5 py-2.5 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all"
                />
              </div>
            ))}
          </div>

          {/* Actions */}
          <div className="flex gap-2 flex-wrap">
            <button onClick={() => setStep(1)} className="flex items-center gap-2 bg-blue-600 text-white text-sm px-4 py-2.5 rounded-xl hover:bg-blue-700 transition-colors font-medium">
              <Book size={14} />
              목차 생성
            </button>
            <button onClick={() => setStep(2)} className="flex items-center gap-2 bg-indigo-600 text-white text-sm px-4 py-2.5 rounded-xl hover:bg-indigo-700 transition-colors font-medium">
              <FileText size={14} />
              챕터 생성
            </button>
            <button onClick={() => setStep(3)} className="flex items-center gap-2 border border-gray-200 text-gray-600 text-sm px-4 py-2.5 rounded-xl hover:bg-gray-50 transition-colors">
              <RefreshCw size={14} />
              일관성 검토
            </button>
            <button onClick={() => setStep(5)} className="flex items-center gap-2 bg-green-600 text-white text-sm px-4 py-2.5 rounded-xl hover:bg-green-700 transition-colors font-medium">
              <Download size={14} />
              Export
            </button>
          </div>
        </div>

        {/* TOC Preview */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="text-sm font-semibold text-gray-800">목차 미리보기</div>
            {step >= 1 && <StatusBadge status="완료" />}
          </div>
          {step >= 1 ? (
            <div className="space-y-1.5">
              <div className="bg-[#0C1B3A] rounded-xl p-3 mb-3">
                <div className="font-semibold text-xs text-white leading-snug">{title}</div>
                <div className="text-blue-300 text-xs mt-1">{docTypes.find((d) => d.id === docType)?.icon} {docTypes.find((d) => d.id === docType)?.label}</div>
              </div>
              {mockToc.map((c) => (
                <div key={c.ch} className="flex items-start gap-2.5 p-2.5 hover:bg-gray-50 rounded-xl transition-colors">
                  <span className="font-mono text-xs text-blue-500 font-bold w-5 flex-shrink-0 mt-0.5">{c.ch}</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-gray-700 font-medium leading-snug">{c.title}</div>
                    <div className="text-xs text-gray-400 mt-0.5">{c.pages}p 예상</div>
                  </div>
                </div>
              ))}
              <div className="pt-2 border-t border-gray-100 text-xs text-gray-400 text-right font-medium">
                총 {mockToc.reduce((a, c) => a + c.pages, 0)}페이지 예상
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-48 text-gray-300">
              <Book size={32} className="mb-3" />
              <div className="text-xs text-center">목차 생성 버튼을 클릭하면<br />미리보기가 표시됩니다</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Gateway Page ─────────────────────────────────────────────────────────────
function GatewayPage() {
  const [toggles, setToggles] = useState({ telegram: true, slack: false, teams: false, web: false });
  const channels = [
    { id: "telegram" as const, name: "Telegram", icon: "✈️", status: "활성", token: "설정됨", lastMsg: "1분 전", adapter: "TelegramAdapter", desc: "현재 long polling으로 메시지를 수신하고 ADK Runner로 전달 중입니다.", bar: "bg-green-500", border: "border-green-200" },
    { id: "slack" as const, name: "Slack", icon: "💬", status: "보류", token: "미설정", lastMsg: "—", adapter: "SlackAdapter", desc: "Slack Bot Token 설정 후 연동 가능. Slack/Teams 확장 예정.", bar: "bg-amber-500", border: "border-amber-200" },
    { id: "teams" as const, name: "Microsoft Teams", icon: "🏢", status: "보류", token: "미설정", lastMsg: "—", adapter: "TeamsAdapter", desc: "Teams Bot Framework 연동 예정. Azure 앱 등록 필요.", bar: "bg-amber-500", border: "border-amber-200" },
    { id: "web" as const, name: "Web (Next.js)", icon: "🌐", status: "스캐폴드", token: "해당 없음", lastMsg: "—", adapter: "WebAdapter", desc: "Next.js 프론트엔드 스캐폴드 준비 완료. API 연동 진행 중.", bar: "bg-purple-500", border: "border-purple-200" },
  ];

  return (
    <div className="p-6 space-y-5">
      <div className="grid grid-cols-2 gap-4">
        {channels.map((ch) => (
          <div key={ch.id} className={`bg-white rounded-2xl border shadow-sm overflow-hidden ${ch.border}`}>
            <div className={`h-1.5 ${ch.bar}`} />
            <div className="p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{ch.icon}</span>
                  <div>
                    <div className="font-semibold text-gray-800">{ch.name}</div>
                    <div className="font-mono text-xs text-gray-400 mt-0.5">{ch.adapter}</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <StatusBadge status={ch.status} />
                  <ToggleSwitch
                    value={toggles[ch.id]}
                    onChange={() => setToggles((p) => ({ ...p, [ch.id]: !p[ch.id] }))}
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-gray-50 rounded-xl px-3 py-2.5">
                  <div className="text-xs text-gray-400">토큰 설정</div>
                  <div className={`text-xs font-semibold mt-0.5 ${ch.token === "설정됨" ? "text-green-600" : "text-gray-500"}`}>{ch.token}</div>
                </div>
                <div className="bg-gray-50 rounded-xl px-3 py-2.5">
                  <div className="text-xs text-gray-400">최근 메시지 수신</div>
                  <div className="text-xs font-semibold text-gray-600 mt-0.5">{ch.lastMsg}</div>
                </div>
              </div>
              <div className="text-xs text-gray-500 leading-relaxed">{ch.desc}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Queue & Heartbeat Page ───────────────────────────────────────────────────
function QueuePage() {
  const queueStats = [
    { label: "대기 중 작업", value: "0", note: "미연동" },
    { label: "실행 중 작업", value: "0", note: "미연동" },
    { label: "실패 작업", value: "0", note: "미연동" },
    { label: "분산락 상태", value: "N/A", note: "스캐폴드" },
  ];
  const hbStats = [
    { label: "Cron Pulse", value: "비활성", note: "미연동" },
    { label: "마지막 변경 감지", value: "—", note: "미연동" },
    { label: "diff_engine", value: "준비 중", note: "스캐폴드" },
    { label: "자동 실행 세션", value: "0", note: "미연동" },
  ];

  return (
    <div className="p-6 space-y-5">
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-red-50 flex items-center justify-center">
              <Database size={18} className="text-red-500" />
            </div>
            <div>
              <div className="font-semibold text-gray-800">Redis Job Queue</div>
              <div className="text-xs text-gray-400 mt-0.5">분산락 기반 작업 큐 관리 시스템</div>
            </div>
          </div>
          <StatusBadge status="스캐폴드" />
        </div>
        <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 text-xs text-amber-700 mb-5 leading-relaxed">
          ⚠️ Redis Queue는 현재 스캐폴드 상태입니다. 실제 Redis 연동 이전에는 작업 큐 기능이 동작하지 않습니다.
        </div>
        <div className="grid grid-cols-4 gap-4">
          {queueStats.map((s) => (
            <div key={s.label} className="bg-gray-50 rounded-2xl p-4 text-center border border-gray-100">
              <div className="text-3xl font-bold text-gray-400 mb-1.5">{s.value}</div>
              <div className="text-xs text-gray-600 font-medium">{s.label}</div>
              <div className="text-xs text-gray-400 mt-1">{s.note}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-blue-50 flex items-center justify-center">
              <Activity size={18} className="text-blue-500" />
            </div>
            <div>
              <div className="font-semibold text-gray-800">Heartbeat 시스템</div>
              <div className="text-xs text-gray-400 mt-0.5">Cron 기반 능동 트리거 및 변경 감지</div>
            </div>
          </div>
          <StatusBadge status="미연동" />
        </div>
        <div className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-xs text-gray-500 mb-5 leading-relaxed">
          ℹ️ Heartbeat 시스템은 현재 미연동 상태입니다. Cron 스케줄러와 diff_engine 연동 후 자동 감지가 시작됩니다.
        </div>
        <div className="grid grid-cols-4 gap-4">
          {hbStats.map((s) => (
            <div key={s.label} className="bg-gray-50 rounded-2xl p-4 text-center border border-gray-100">
              <div className="text-2xl font-bold text-gray-400 mb-1.5">{s.value}</div>
              <div className="text-xs text-gray-600 font-medium">{s.label}</div>
              <div className="text-xs text-gray-400 mt-1">{s.note}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-gradient-to-r from-[#0C1B3A] to-[#1E3A6E] rounded-2xl p-5 text-white">
        <div className="font-semibold mb-3">인프라 로드맵</div>
        <div className="grid grid-cols-3 gap-4">
          {[
            { phase: "Phase 1 ✅", desc: "Telegram + ADK Runner + Root Agent 기본 연동", status: "완료" },
            { phase: "Phase 2 🔄", desc: "Redis Queue + 분산락 + 작업 큐 시스템 연동", status: "진행 예정" },
            { phase: "Phase 3 📋", desc: "Heartbeat + diff_engine + 자동 Agent 트리거", status: "계획 중" },
          ].map((p) => (
            <div key={p.phase} className="bg-white/10 rounded-xl p-4">
              <div className="font-semibold text-blue-200 text-sm mb-1.5">{p.phase}</div>
              <div className="text-blue-100 text-xs leading-relaxed">{p.desc}</div>
              <div className="mt-2 text-blue-300 text-xs font-medium">{p.status}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Logs Page ────────────────────────────────────────────────────────────────
function LogsPage() {
  const [filter, setFilter] = useState("전체");
  const filters = ["전체", "Gateway", "Runner", "Root Agent", "Transfer", "Tool Call", "Error"];
  const layerStyle: Record<string, string> = {
    Gateway: "bg-blue-50 text-blue-700 border-blue-100",
    Runner: "bg-indigo-50 text-indigo-700 border-indigo-100",
    "Root Agent": "bg-violet-50 text-violet-700 border-violet-100",
    Transfer: "bg-purple-50 text-purple-700 border-purple-100",
    "Tool Call": "bg-amber-50 text-amber-700 border-amber-100",
    Error: "bg-red-50 text-red-700 border-red-100",
  };
  const filtered = filter === "전체" ? allLogs : allLogs.filter((l) => l.layer === filter);

  return (
    <div className="p-6 space-y-5">
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-gray-100 flex-wrap gap-2">
          <div className="flex gap-1 flex-wrap">
            {filters.map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`text-xs px-3 py-1.5 rounded-lg transition-colors font-medium ${
                  filter === f ? "bg-blue-600 text-white" : "text-gray-500 hover:bg-gray-100"
                }`}
              >
                {f}
                {f !== "전체" && (
                  <span className="ml-1 opacity-60">({allLogs.filter((l) => l.layer === f).length})</span>
                )}
              </button>
            ))}
          </div>
          <button className="flex items-center gap-1.5 text-xs text-gray-500 border border-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors">
            <Download size={12} />
            로그 내보내기
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-gray-100 bg-gray-50">
                {["시간", "레이어", "이벤트", "Agent", "상태", "상세"].map((h) => (
                  <th key={h} className="text-left px-4 py-3 text-gray-500 font-semibold whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {filtered.map((l, i) => (
                <tr key={i} className={`hover:bg-gray-50/60 transition-colors ${l.status === "실패" ? "bg-red-50/20" : ""}`}>
                  <td className="px-4 py-3 font-mono text-gray-400 whitespace-nowrap">{l.time}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-md text-xs font-medium border ${layerStyle[l.layer] ?? "bg-gray-100 text-gray-600 border-gray-200"}`}>
                      {l.layer}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-700">{l.event}</td>
                  <td className="px-4 py-3 font-mono text-blue-600">{l.agent}</td>
                  <td className="px-4 py-3"><StatusBadge status={l.status} /></td>
                  <td className="px-4 py-3 text-gray-400 font-mono">{l.detail}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ─── Settings Page ────────────────────────────────────────────────────────────
function SettingsPage() {
  const [channels, setChannels] = useState({ telegram: true, slack: false, teams: false, web: false });
  const [model, setModel] = useState("ollama");
  const [debug, setDebug] = useState(false);
  const [lang, setLang] = useState("ko");
  const [hideReasoning, setHideReasoning] = useState(true);

  return (
    <div className="p-6 space-y-5 max-w-3xl">
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="text-sm font-semibold text-gray-800 mb-0.5">채널 설정 (channels.yaml)</div>
        <div className="text-xs text-gray-400 mb-4">외부 채널 연결 상태를 관리합니다</div>
        <div className="space-y-0 divide-y divide-gray-50">
          {[
            { id: "telegram" as const, name: "Telegram", desc: "Long polling 방식 — 현재 활성 상태" },
            { id: "slack" as const, name: "Slack", desc: "Slack Bot Token 필요 — 확장 예정" },
            { id: "teams" as const, name: "Microsoft Teams", desc: "Azure 앱 등록 필요 — 확장 예정" },
            { id: "web" as const, name: "Web (Next.js)", desc: "API 연동 진행 중 — 스캐폴드 상태" },
          ].map(({ id, name, desc }) => (
            <div key={id} className="flex items-center justify-between py-3.5">
              <div>
                <div className="text-sm font-medium text-gray-700">{name}</div>
                <div className="text-xs text-gray-400 mt-0.5">{desc}</div>
              </div>
              <ToggleSwitch value={channels[id]} onChange={() => setChannels((p) => ({ ...p, [id]: !p[id] }))} />
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="text-sm font-semibold text-gray-800 mb-0.5">모델 설정</div>
        <div className="text-xs text-gray-400 mb-4">AI 모델 공급자를 선택합니다</div>
        <div className="space-y-2">
          {[
            { id: "ollama", name: "Ollama (로컬)", desc: "gemma4:31b — 현재 사용 중", badge: "로컬" },
            { id: "google", name: "Google AI Studio", desc: "gemini-2.0-flash-exp", badge: "클라우드" },
            { id: "vertex", name: "Vertex AI", desc: "google/gemini-2.5-pro", badge: "클라우드" },
          ].map((m) => (
            <label
              key={m.id}
              className={`flex items-center gap-3 p-3.5 rounded-xl border cursor-pointer transition-all ${
                model === m.id ? "border-blue-400 bg-blue-50" : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
              }`}
            >
              <input type="radio" name="model" value={m.id} checked={model === m.id} onChange={() => setModel(m.id)} className="accent-blue-600" />
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-700">{m.name}</div>
                <div className="text-xs text-gray-400 mt-0.5 font-mono">{m.desc}</div>
              </div>
              <span className="text-xs px-2.5 py-1 bg-gray-100 text-gray-500 rounded-full font-medium">{m.badge}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div className="text-sm font-semibold text-gray-800 mb-0.5">고급 설정</div>
        <div className="text-xs text-gray-400 mb-4">시스템 동작 방식을 설정합니다</div>
        <div className="space-y-0 divide-y divide-gray-50">
          <div className="flex items-center justify-between py-3.5">
            <div>
              <div className="text-sm font-medium text-gray-700">AGENT_DEBUG 모드</div>
              <div className="text-xs text-gray-400 mt-0.5">상세 디버그 로그 출력 활성화</div>
            </div>
            <ToggleSwitch value={debug} onChange={() => setDebug(!debug)} />
          </div>
          <div className="flex items-center justify-between py-3.5">
            <div>
              <div className="text-sm font-medium text-gray-700">응답 언어</div>
              <div className="text-xs text-gray-400 mt-0.5">Agent 응답 언어 설정</div>
            </div>
            <select
              value={lang}
              onChange={(e) => setLang(e.target.value)}
              className="text-sm border border-gray-200 rounded-xl px-3 py-1.5 outline-none focus:border-blue-400 bg-white"
            >
              <option value="ko">한국어</option>
              <option value="en">English</option>
            </select>
          </div>
          <div className="flex items-center justify-between py-3.5">
            <div>
              <div className="text-sm font-medium text-gray-700">추론 과정 노출 방지</div>
              <div className="text-xs text-gray-400 mt-0.5">최종 응답만 사용자에게 전달 (추론 과정 숨김)</div>
            </div>
            <ToggleSwitch value={hideReasoning} onChange={() => setHideReasoning(!hideReasoning)} />
          </div>
        </div>
      </div>

      <button className="bg-blue-600 text-white text-sm px-6 py-2.5 rounded-xl hover:bg-blue-700 transition-colors font-semibold">
        설정 저장
      </button>
    </div>
  );
}

// ─── App ──────────────────────────────────────────────────────────────────────
export default function App() {
  const [page, setPage] = useState<Page>("dashboard");

  const renderPage = () => {
    switch (page) {
      case "dashboard": return <DashboardPage setPage={setPage} />;
      case "tasks": return <TasksPage />;
      case "agents": return <AgentsPage setPage={setPage} />;
      case "agent-detail": return <AgentDetailPage setPage={setPage} />;
      case "book-agent": return <BookAgentPage />;
      case "gateway": return <GatewayPage />;
      case "queue": return <QueuePage />;
      case "logs": return <LogsPage />;
      case "settings": return <SettingsPage />;
      default: return null;
    }
  };

  return (
    <div className="flex h-screen bg-[#F0F2F7] overflow-hidden" style={{ fontFamily: "'Noto Sans KR', sans-serif" }}>
      <Sidebar page={page} setPage={setPage} />
      <div className="flex-1 ml-60 flex flex-col min-h-0">
        <Header page={page} />
        <main className="flex-1 overflow-y-auto">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}
