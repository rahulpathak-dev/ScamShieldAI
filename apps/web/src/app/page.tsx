import Link from "next/link";
import {
  AlertTriangle,
  ArrowRight,
  BadgeCheck,
  BrainCircuit,
  CheckCircle2,
  DatabaseZap,
  FileWarning,
  Fingerprint,
  Globe2,
  KeyRound,
  LockKeyhole,
  MailWarning,
  Radar,
  ScanSearch,
  ShieldCheck,
  ShieldEllipsis,
  Sparkles
} from "lucide-react";

const features = [
  { title: "Message, email, and URL scanning", description: "Paste suspicious content and receive a structured scam assessment in seconds.", icon: ScanSearch },
  { title: "Risk scoring", description: "Classifies risk as low, medium, high, or critical with a 0-100 score.", icon: Radar },
  { title: "Persuasion detection", description: "Finds urgency, fear, fake authority, greed, scarcity, and impersonation tactics.", icon: BrainCircuit },
  { title: "Threat intelligence", description: "Correlates suspicious keywords, links, phone numbers, and reported scam patterns.", icon: DatabaseZap }
];

const workflow = [
  "Paste suspicious message, email, chat, or link",
  "NLP engine extracts scam and persuasion signals",
  "Risk engine combines evidence into a severity score",
  "AI explanation gives safety recommendations"
];

const scamTypes = ["Phishing", "Banking fraud", "Crypto scams", "Investment scams", "Romance scams", "Job scams", "Lottery scams", "Identity theft"];
const techStack = ["Next.js", "TypeScript", "Tailwind CSS", "FastAPI", "PostgreSQL", "SQLAlchemy", "Transformers", "Docker"];
const trustSignals = ["No hardcoded secrets", "PostgreSQL persistence", "Secure headers", "Rate limiting", "Input validation", "JWT-ready auth"];
const useCases = [
  { title: "Consumers", description: "Check suspicious bank alerts, job offers, lottery messages, and unknown links before responding." },
  { title: "Security teams", description: "Triage scam reports, review high-risk patterns, and preserve audit-friendly scan history." },
  { title: "Enterprises", description: "Use API-first analysis for customer support, fraud operations, and trust and safety workflows." }
];

const faqs = [
  { question: "Does ScamShieldAI store the full message?", answer: "The API stores structured scan evidence and a content hash for history. The UI avoids exposing raw sensitive content in database history." },
  { question: "Can it detect URLs and emails?", answer: "Yes. The scanner accepts suspicious SMS, email, chat, and URL-style text and analyzes scam indicators." },
  { question: "Is this production-ready?", answer: "The project includes secure configuration, Docker, PostgreSQL migrations, API docs, GitHub workflows, and deployment guidance." },
  { question: "Can I deploy it to cloud platforms?", answer: "Yes. The README documents frontend, backend, database, Docker, and production environment setup paths." }
];


export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <header className="sticky top-0 z-20 border-b border-white/10 bg-slate-950/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-teal-400 text-slate-950">
              <ShieldCheck className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-bold uppercase tracking-wide text-white">ScamShieldAI</p>
              <p className="text-xs text-slate-400">AI scam defense platform</p>
            </div>
          </Link>
          <nav className="flex items-center gap-2">
            <Link className="hidden rounded-md px-3 py-2 text-sm font-medium text-slate-300 hover:bg-white/10 sm:inline-flex" href="/login">
              Login
            </Link>
            <Link className="inline-flex h-10 items-center justify-center rounded-md bg-teal-400 px-4 text-sm font-semibold text-slate-950 hover:bg-teal-300" href="/register">
              Start scanning
            </Link>
          </nav>
        </div>
      </header>

      <section className="mx-auto grid max-w-7xl gap-10 px-4 py-12 sm:px-6 lg:grid-cols-[0.95fr_1.05fr] lg:px-8 lg:py-16">
        <div className="flex flex-col justify-center">
          <div className="mb-5 flex w-fit items-center gap-2 rounded-full border border-amber-300/30 bg-amber-300/10 px-3 py-1 text-sm font-medium text-amber-100">
            <AlertTriangle className="h-4 w-4" aria-hidden="true" />
            Real-time scam detection for financial threats
          </div>
          <h1 className="max-w-3xl text-4xl font-bold tracking-normal text-white sm:text-5xl lg:text-6xl">
            Detect scams before they steal trust, money, or identity.
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-300">
            ScamShieldAI analyzes suspicious messages, emails, links, ads, and chats with NLP, explainable AI, and threat intelligence so users know what is dangerous and why.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link className="inline-flex h-11 items-center justify-center rounded-md bg-teal-400 px-5 text-sm font-semibold text-slate-950 hover:bg-teal-300" href="/analyzer">
              Paste suspicious message and scan
              <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" />
            </Link>
            <Link className="inline-flex h-11 items-center justify-center rounded-md border border-white/15 bg-white/5 px-5 text-sm font-semibold text-white hover:bg-white/10" href="/dashboard">
              Open dashboard
            </Link>
          </div>
        </div>

        <div className="rounded-lg border border-white/10 bg-white/[0.03] p-4 shadow-2xl shadow-teal-950/40">
          <div className="rounded-md border border-white/10 bg-slate-900 p-4">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <div>
                <p className="text-sm font-semibold text-white">Live Scan Console</p>
                <p className="text-xs text-slate-400">Text, email, URL, and chat analysis</p>
              </div>
              <span className="rounded-md bg-red-500/15 px-2 py-1 text-xs font-semibold text-red-200">Critical</span>
            </div>
            <div className="mt-4 grid gap-4 md:grid-cols-[1fr_180px]">
              <div className="rounded-md border border-white/10 bg-white/5 p-3">
                <p className="text-xs uppercase tracking-wide text-slate-400">Suspicious input</p>
                <p className="mt-3 text-sm leading-6 text-slate-200">
                  Urgent bank alert: verify your OTP now or your account will be suspended. Open secure-verify link immediately.
                </p>
              </div>
              <div className="rounded-md border border-red-400/30 bg-red-500/10 p-3">
                <p className="text-xs uppercase tracking-wide text-red-200">Risk score</p>
                <p className="mt-2 text-4xl font-bold text-white">94</p>
                <p className="text-sm text-red-100">Critical scam probability</p>
              </div>
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              {["Urgency", "Bank impersonation", "OTP request"].map((item) => (
                <div key={item} className="flex items-center gap-2 rounded-md border border-white/10 bg-white/5 p-3 text-sm text-slate-200">
                  <CheckCircle2 className="h-4 w-4 text-teal-300" aria-hidden="true" />
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-white/10 bg-white/[0.03] py-12">
        <div className="mx-auto grid max-w-7xl gap-4 px-4 sm:px-6 md:grid-cols-2 lg:grid-cols-4 lg:px-8">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <article key={feature.title} className="rounded-md border border-white/10 bg-slate-900/80 p-5">
                <Icon className="h-5 w-5 text-teal-300" aria-hidden="true" />
                <h2 className="mt-4 text-base font-semibold text-white">{feature.title}</h2>
                <p className="mt-2 text-sm leading-6 text-slate-400">{feature.description}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-2 lg:px-8">
        <div>
          <div className="flex items-center gap-2 text-teal-300">
            <ShieldEllipsis className="h-5 w-5" aria-hidden="true" />
            <span className="text-sm font-semibold uppercase tracking-wide">How it works</span>
          </div>
          <h2 className="mt-3 text-3xl font-bold text-white">Explainable security workflow</h2>
          <div className="mt-6 grid gap-3">
            {workflow.map((item, index) => (
              <div key={item} className="flex items-center gap-3 rounded-md border border-white/10 bg-white/[0.03] p-4">
                <span className="flex h-8 w-8 items-center justify-center rounded-md bg-teal-400 text-sm font-bold text-slate-950">{index + 1}</span>
                <span className="font-medium text-slate-200">{item}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-md border border-white/10 bg-white/[0.03] p-6">
          <div className="flex items-center gap-2 text-amber-200">
            <FileWarning className="h-5 w-5" aria-hidden="true" />
            <span className="text-sm font-semibold uppercase tracking-wide">Scam types detected</span>
          </div>
          <div className="mt-5 flex flex-wrap gap-2">
            {scamTypes.map((item) => (
              <span key={item} className="rounded-md border border-white/10 bg-slate-900 px-3 py-2 text-sm font-medium text-slate-200">
                {item}
              </span>
            ))}
          </div>
          <div className="mt-6 rounded-md border border-teal-300/20 bg-teal-300/10 p-4">
            <div className="flex items-center gap-2 text-teal-100">
              <Sparkles className="h-4 w-4" aria-hidden="true" />
              <h3 className="text-sm font-semibold">AI explanation</h3>
            </div>
            <p className="mt-2 text-sm leading-6 text-slate-300">
              ScamShieldAI explains suspicious findings in plain language, such as urgency, sensitive information requests, fake authority, malicious links, and recommended next steps.
            </p>
          </div>
        </div>
      </section>

      <section className="border-y border-white/10 bg-slate-900/70 py-12">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 sm:px-6 lg:grid-cols-2 lg:px-8">
          <div>
            <div className="flex items-center gap-2 text-teal-300">
              <LockKeyhole className="h-5 w-5" aria-hidden="true" />
              <span className="text-sm font-semibold uppercase tracking-wide">Trust and security</span>
            </div>
            <h2 className="mt-3 text-3xl font-bold text-white">Built with production security practices</h2>
            <p className="mt-4 text-sm leading-6 text-slate-400">
              The platform uses environment-based secrets, API validation, CORS configuration, secure headers, SQLAlchemy parameterization, safe errors, and privacy-aware logging.
            </p>
            <div className="mt-5 grid gap-2 sm:grid-cols-2">
              {trustSignals.map((item) => (
                <div key={item} className="flex items-center gap-2 rounded-md border border-white/10 bg-white/[0.03] p-3 text-sm text-slate-200">
                  <BadgeCheck className="h-4 w-4 text-teal-300" aria-hidden="true" />
                  {item}
                </div>
              ))}
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2 text-teal-300">
              <Globe2 className="h-5 w-5" aria-hidden="true" />
              <span className="text-sm font-semibold uppercase tracking-wide">Tech stack</span>
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              {techStack.map((item) => (
                <span key={item} className="rounded-md border border-white/10 bg-slate-950 px-3 py-2 text-sm font-medium text-slate-200">
                  {item}
                </span>
              ))}
            </div>
            <div className="mt-6 grid gap-3 sm:grid-cols-3">
              <MiniMetric icon={KeyRound} label="Auth" value="JWT-ready" />
              <MiniMetric icon={Fingerprint} label="Signals" value="NLP + rules" />
              <MiniMetric icon={MailWarning} label="Alerts" value="High-risk" />
            </div>
          </div>
        </div>
      </section>


      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-300">Use cases</p>
          <h2 className="mt-3 text-3xl font-bold text-white">Built for everyday users and security workflows</h2>
          <p className="mt-3 text-sm leading-6 text-slate-400">
            ScamShieldAI is designed for browser-first scam checking, but the architecture also supports analyst dashboards, alerting, extensions, mobile flows, and enterprise APIs.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {useCases.map((item) => (
            <article key={item.title} className="rounded-md border border-white/10 bg-white/[0.03] p-5">
              <h3 className="text-base font-semibold text-white">{item.title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-400">{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="border-y border-white/10 bg-white/[0.03] py-12">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:px-8">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-teal-300">FAQ</p>
            <h2 className="mt-3 text-3xl font-bold text-white">Common questions</h2>
            <p className="mt-3 text-sm leading-6 text-slate-400">Quick answers for users, reviewers, and recruiters opening the project for the first time.</p>
          </div>
          <div className="grid gap-3">
            {faqs.map((item) => (
              <article key={item.question} className="rounded-md border border-white/10 bg-slate-950 p-4">
                <h3 className="text-sm font-semibold text-white">{item.question}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-400">{item.answer}</p>
              </article>
            ))}
          </div>
        </div>
      </section>
      <footer className="px-4 py-8 text-center text-sm text-slate-400">
        <p className="font-semibold text-white">ScamShieldAI</p>
        <p className="mt-2">NLP, explainable AI, and threat intelligence for safer digital finance.</p>
        <p className="mt-3">Contact: security@scamshieldai.example</p>
      </footer>
    </main>
  );
}

function MiniMetric({ icon: Icon, label, value }: { icon: typeof ShieldCheck; label: string; value: string }) {
  return (
    <div className="rounded-md border border-white/10 bg-white/[0.03] p-4">
      <Icon className="h-5 w-5 text-teal-300" aria-hidden="true" />
      <p className="mt-3 text-xs uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-1 text-sm font-semibold text-white">{value}</p>
    </div>
  );
}