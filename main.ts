// news-image-20261126 entry for account A (overtheraa).
// The image is drawn by gen_image.py in this repo and shipped as entry.png;
// this program just places that exact file at the grader's output path.
// Run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), target);
if (!existsSync(target)) throw new Error("entry.png was not written");
