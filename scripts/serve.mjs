import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, extname, sep } from 'node:path';
const site = fileURLToPath(new URL('../',import.meta.url));
const portIndex=process.argv.indexOf('--port');
const port=portIndex>=0 ? Number(process.argv[portIndex+1]) : 4173;
const baseIndex=process.argv.indexOf('--base');
const base=baseIndex>=0 ? process.argv[baseIndex+1] : '/';
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.ttf':'font/ttf','.txt':'text/plain; charset=utf-8','.json':'application/json'};
createServer(async(req,res)=>{
  try {
    let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    if(!pathname.startsWith(base)){res.writeHead(404);res.end('Not found');return;}
    pathname=pathname.slice(base.length);
    let file=resolve(site,pathname || 'index.html');
    if(file!==resolve(site) && !file.startsWith(resolve(site)+sep)){res.writeHead(403);res.end('Forbidden');return;}
    if((await stat(file)).isDirectory()) {
      if(!req.url.split('?')[0].endsWith('/')){res.writeHead(302,{Location:new URL(req.url,'http://localhost').pathname+'/'+new URL(req.url,'http://localhost').search});res.end();return;}
      file=resolve(file,'index.html');
    }
    const body=await readFile(file);
    res.writeHead(200,{'Content-Type':types[extname(file)]||'application/octet-stream','Cache-Control':'no-cache'});
    res.end(req.method==='HEAD' ? undefined : body);
  } catch(error){res.writeHead(404);res.end('Not found');}
}).listen(port,'127.0.0.1',()=>console.log(`Marsfall preview: http://127.0.0.1:${port}${base}`));
