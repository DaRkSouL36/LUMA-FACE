import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/COMPONENTS/LAYOUT/navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FACE RESTORATION AI",
  description: "RESTORE AND ENHANCE FACE IMAGES USING GFPGAN AND REAL-ESRGAN.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <Navbar />
        <main className="min-h-screen bg-background text-foreground">
          {children}
        </main>
      </body>
    </html>
  );
}
