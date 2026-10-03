import { mkdir, writeFile, cp } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, join } from 'node:path';
import { pageTemplate } from '../src/page-templates.mjs';

const site = fileURLToPath(new URL('../', import.meta.url));
const sourceOnly = process.argv.includes('--source-only');
for (const [page, file] of [['home','index.html'],['arsenal','arsenal/index.html'],['renders','renders/index.html']]) {
  const target = join(site,file);
  await mkdir(resolve(target,'..'), {recursive:true});
  await writeFile(target, pageTemplate(page));
}
if (!sourceOnly) {
  const output = join(site,'dist');
  await mkdir(output,{recursive:true});
  for (const entry of ['index.html','arsenal','renders','assets','favicon.svg','.nojekyll']) {
    await cp(join(site,entry),join(output,entry),{recursive:true});
  }
  await mkdir(join(output,'src'),{recursive:true});
  for (const file of ['app.js','content.js','styles.css']) await cp(join(site,'src',file),join(output,'src',file));
}
console.log(sourceOnly ? 'Generated three static pages.' : 'Built three routes and all assets into dist/.');
