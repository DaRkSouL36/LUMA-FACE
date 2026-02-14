import Link from "next/link";
import { Cpu, Github, Linkedin } from "lucide-react"; // ADDED LINKEDIN ICON

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 border-b border-white/10 bg-background/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* LOGO AREA */}
          <div className="flex items-center gap-2">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Cpu className="w-6 h-6 text-primary" />
            </div>
            <Link href="/" className="font-bold text-xl tracking-tight">
              FACERESTORE<span className="text-primary">.AI</span>
            </Link>
          </div>

          {/* RIGHT ACTIONS */}
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/DaRkSouL36"
              target="_blank"
              rel="noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
            {/* LINKEDIN ADDED HERE */}
            <a
              href="https://www.linkedin.com/in/nextgenml/"
              target="_blank"
              rel="noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <Linkedin className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}