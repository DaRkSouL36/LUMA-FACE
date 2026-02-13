import Link from "next/link";
import { ArrowRight, Cpu, Layers, ScanFace } from "lucide-react";
import { Button } from "@/COMPONENTS/UI/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/COMPONENTS/UI/card";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-black text-white selection:bg-white/20">
      {/* HERO SECTION */}
      <section className="flex-1 flex flex-col items-center justify-center py-32 px-4 text-center space-y-8">
        {/* STATUS BADGE */}
        <div className="inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-bold tracking-widest text-zinc-400 uppercase backdrop-blur-xl">
          <span className="flex h-1.5 w-1.5 rounded-full bg-green-500 mr-2 animate-pulse"></span>
          DaRKSouL
        </div>

        {/* HEADLINE */}
        <div className="space-y-6 max-w-4xl">
          <h1 className="text-5xl md:text-8xl font-black tracking-tighter text-white uppercase leading-[0.9]">
            Restore Identity. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-white/40">
              Pixel by Pixel.
            </span>
          </h1>
          <p className="text-sm md:text-lg text-zinc-400 max-w-2xl mx-auto uppercase tracking-widest leading-relaxed">
            A state-of-the-art Deep Learning pipeline for Blind Face Restoration
            and Super-Resolution.
            <br className="hidden md:block" />
            <span className="text-zinc-600">
              Align. Detect. Restore. Enhance. Verify.
            </span>
          </p>
        </div>

        {/* CALL TO ACTION - THIS LINKS TO THE APP */}
        <div className="flex flex-col sm:flex-row gap-4 pt-8">
          <Link href="/ENHANCE">
            <Button size="lg" className="w-full sm:w-auto text-base h-14 px-8">
              START RESTORING <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </Link>
          <a
            href="https://github.com/DaRkSouL36/FACE-IMAGE-ENHANCEMENT-AND-RESTORATION"
            target="_blank"
            rel="noreferrer"
          >
            <Button
              variant="outline"
              size="lg"
              className="w-full sm:w-auto text-base h-14 px-8"
            >
              VIEW GITHUB
            </Button>
          </a>
        </div>
      </section>

      {/* FEATURE GRID */}
      <section className="py-24 px-4 border-t border-white/5 bg-zinc-950/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* FEATURE 1 */}
            <Card className="bg-transparent border-white/10 hover:bg-white/5 transition-colors duration-500">
              <CardHeader>
                <ScanFace className="w-8 h-8 text-white mb-4" />
                <CardTitle>Blind Restoration</CardTitle>
              </CardHeader>
              <CardContent className="text-sm leading-relaxed tracking-wide">
                LEVERAGING <strong>GFPGAN</strong> PRIORS TO RECOVER FACIAL
                GEOMETRY FROM SEVERELY DEGRADED INPUTS WITHOUT GROUND TRUTH
                REFERENCES.
              </CardContent>
            </Card>

            {/* FEATURE 2 */}
            <Card className="bg-transparent border-white/10 hover:bg-white/5 transition-colors duration-500">
              <CardHeader>
                <Layers className="w-8 h-8 text-white mb-4" />
                <CardTitle>4x Super-Resolution</CardTitle>
              </CardHeader>
              <CardContent className="text-sm leading-relaxed tracking-wide">
                INTEGRATED <strong>REAL-ESRGAN</strong> UPSCALING ENSURES SHARP
                BACKGROUNDS AND HAIR TEXTURES, ELIMINATING THE `PASTE-ON` EFFECT.
              </CardContent>
            </Card>

            {/* FEATURE 3 */}
            <Card className="bg-transparent border-white/10 hover:bg-white/5 transition-colors duration-500">
              <CardHeader>
                <Cpu className="w-8 h-8 text-white mb-4" />
                <CardTitle>Identity Verification</CardTitle>
              </CardHeader>
              <CardContent className="text-sm leading-relaxed tracking-wide">
                BUILT-IN <strong>INSIGHTFACE</strong> ANALYSIS COMPUTES COSINE
                SIMILARITY TO ENSURE THE RESTORED FACE MATCHES THE ORIGINAL
                IDENTITY.
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
}
