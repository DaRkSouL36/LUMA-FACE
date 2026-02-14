import { Github, Linkedin } from "lucide-react"; // REMOVED UNUSED TWITTER, ADDED LINKEDIN

export default function Footer() {
  return (
    <footer className="w-full border-t border-white/10 bg-black py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-col items-center md:items-start">
          <span className="text-lg font-bold tracking-tighter uppercase text-white">
            FACERESTORE<span className="text-zinc-500">.AI</span>
          </span>
          <p className="text-[10px] text-zinc-500 uppercase mt-1 tracking-widest">
            IDENTITY-PRESERVING FACE RESTORATION
          </p>
        </div>

        {/* SOCIAL LINKS AREA */}
        <div className="flex items-center gap-6">
          <a
            href="https://github.com/DaRkSouL36"
            target="_blank"
            rel="noreferrer"
            className="text-zinc-400 hover:text-white transition-colors"
          >
            <Github className="w-5 h-5" />
          </a>
          {/* LINKEDIN ADDED HERE */}
          <a
            href="https://www.linkedin.com/in/nextgenml/"
            target="_blank"
            rel="noreferrer"
            className="text-zinc-400 hover:text-white transition-colors"
          >
            <Linkedin className="w-5 h-5" />
          </a>
        </div>

        <div className="text-[10px] text-zinc-600 uppercase tracking-widest">
          © 2026 SHARAD SHAHI.
        </div>
      </div>
    </footer>
  );
}
