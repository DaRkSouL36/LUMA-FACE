import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,

  // OVERRIDE DEFAULT IGNORES FROM ESLINT-CONFIG-NEXT
  globalIgnores([
    // DEFAULT IGNORES PROVIDED BY ESLINT-CONFIG-NEXT
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
]);

export default eslintConfig;
