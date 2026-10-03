import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { catalogue, gallery } from '../src/content.js';
import { siteConfig } from '../src/site-config.js';
const site=fileURLToPath(new URL('../',import.meta.url));
for(const list of [catalogue,gallery]){
  assert.equal(new Set(list.map(x=>x.id)).size,list.length,'Duplicate archive identifiers');
  for(const item of list){assert(item.description && (item.name||item.title));assert((await stat(resolve(site,item.image))).size>0,'Missing artwork: '+item.image);}
}
assert.equal(siteConfig.price,5);
assert.equal(siteConfig.demoMissions,6);
assert(new URL(siteConfig.purchaseUrl).protocol==='https:');
if(siteConfig.demoUrl) assert(new URL(siteConfig.demoUrl).protocol==='https:','Use an HTTPS demo link');
for(const file of ['index.html','arsenal/index.html','renders/index.html']){
  const html=await readFile(resolve(site,file),'utf8');
  assert(html.includes('<title>') && html.includes('name="description"'),'Missing page metadata');
  assert(html.includes('id="main"') && html.includes('Skip to content'));
  assert(!/href="#"/.test(html),'Placeholder link');
  for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){
    const link=match[1].split('#')[0].split('?')[0];
    if(!link || /^(https:|mailto:|data:)/.test(link)) continue;
    const target=resolve(site,file,'..',link);
    await stat(target).catch(()=>assert.fail(`Broken link in ${file}: ${link}`));
  }
}
console.log(`PASS: ${catalogue.length} catalogue entries, ${gallery.length} gallery pieces, three pages, all local links/assets, $5 purchase and six-mission demo configuration.`);
