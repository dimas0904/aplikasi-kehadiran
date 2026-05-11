from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///kehadiran.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Kehadiran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    waktu_absen = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ─── SHARED STYLE & NAV ───────────────────────────────────────────────────────
BASE_STYLE = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --blue:#2563EB;--blue-l:#EFF6FF;--blue-m:#BFDBFE;
  --green:#16A34A;--green-l:#F0FDF4;--green-m:#BBF7D0;
  --red:#DC2626;--red-l:#FEF2F2;--red-m:#FECACA;
  --yellow:#D97706;--yellow-l:#FFFBEB;--yellow-m:#FDE68A;
  --teal:#0D9488;--teal-l:#F0FDFA;--teal-m:#99F6E4;
  --g50:#F9FAFB;--g100:#F3F4F6;--g200:#E5E7EB;--g300:#D1D5DB;
  --g400:#9CA3AF;--g500:#6B7280;--g600:#4B5563;--g800:#1F2937;--g900:#111827;
  --r:12px;--rs:8px;--sh:0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.04);
  --shm:0 4px 6px -1px rgba(0,0,0,.07),0 2px 4px -1px rgba(0,0,0,.04);
}
body{font-family:'Plus Jakarta Sans',sans-serif;background:#F1F5F9;color:var(--g900);min-height:100vh}
/* HEADER */
header{background:linear-gradient(135deg,#1E40AF 0%,#2563EB 50%,#3B82F6 100%);color:#fff;position:sticky;top:0;z-index:100;box-shadow:0 2px 12px rgba(37,99,235,.3)}
.hdr{max-width:1100px;margin:0 auto;padding:.875rem 1.5rem;display:flex;align-items:center;justify-content:space-between}
.hdr-left{display:flex;align-items:center;gap:12px}
.hdr-icon{width:40px;height:40px;background:rgba(255,255,255,.2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}
.hdr-title{font-size:17px;font-weight:700}
.hdr-sub{font-size:12px;opacity:.8;margin-top:1px}
.hdr-badge{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:4px 12px;font-size:12px;font-weight:500}
/* NAV TABS */
nav{background:#1D4ED8;border-bottom:1px solid rgba(255,255,255,.1)}
.nav-inner{max-width:1100px;margin:0 auto;padding:0 1.5rem;display:flex;gap:4px}
.nav-tab{display:flex;align-items:center;gap:7px;padding:10px 16px;color:rgba(255,255,255,.7);font-size:13px;font-weight:500;text-decoration:none;border-bottom:3px solid transparent;transition:all .15s;cursor:pointer;border-top:none;border-left:none;border-right:none;background:none;font-family:inherit}
.nav-tab:hover{color:#fff;background:rgba(255,255,255,.08)}
.nav-tab.active{color:#fff;border-bottom-color:#fff;font-weight:600}
/* MAIN */
.main{max-width:1100px;margin:0 auto;padding:1.5rem}
/* CARD */
.card{background:#fff;border-radius:var(--r);box-shadow:var(--sh);border:1px solid var(--g200);overflow:hidden;margin-bottom:1.5rem}
.card-hdr{padding:1.125rem 1.5rem;border-bottom:1px solid var(--g100);display:flex;align-items:center;gap:10px}
.card-hdr-icon{width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px}
.card-hdr-icon.blue{background:var(--blue-l)}
.card-hdr-icon.green{background:var(--green-l)}
.card-hdr-icon.teal{background:var(--teal-l)}
.card-hdr-icon.red{background:var(--red-l)}
.card-title{font-size:15px;font-weight:600;color:var(--g800)}
.card-sub{font-size:12px;color:var(--g400);margin-top:1px}
.card-body{padding:1.5rem}
/* GRID */
.grid2{display:grid;grid-template-columns:370px 1fr;gap:1.5rem;align-items:start}
@media(max-width:800px){.grid2{grid-template-columns:1fr}}
/* STATS */
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin-bottom:1.25rem}
.stat{background:var(--g50);border:1px solid var(--g200);border-radius:var(--rs);padding:.875rem;text-align:center}
.stat-num{font-size:24px;font-weight:700;line-height:1}
.stat-lbl{font-size:11px;color:var(--g400);margin-top:4px;font-weight:500;text-transform:uppercase;letter-spacing:.04em}
.stat.hadir .stat-num{color:var(--green)}
.stat.alpha .stat-num{color:var(--red)}
.stat.izin .stat-num{color:var(--yellow)}
/* FORM */
.form-group{display:flex;flex-direction:column;gap:6px;margin-bottom:1rem}
label{font-size:13px;font-weight:600;color:var(--g600)}
input,select{padding:10px 14px;border:1.5px solid var(--g200);border-radius:var(--rs);font-size:14px;font-family:inherit;color:var(--g900);background:var(--g50);transition:all .15s;outline:none}
input:focus,select:focus{border-color:var(--blue);background:#fff;box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.btn{padding:11px 20px;border:none;border-radius:var(--rs);font-size:14px;font-weight:600;cursor:pointer;transition:all .15s;font-family:inherit;display:inline-flex;align-items:center;justify-content:center;gap:8px}
.btn-primary{background:var(--blue);color:#fff;width:100%}
.btn-primary:hover{background:#1D4ED8;transform:translateY(-1px);box-shadow:var(--shm)}
.btn-primary:active{transform:translateY(0)}
/* ALERT */
.alert{padding:12px 16px;border-radius:var(--rs);font-size:13px;font-weight:500;margin-bottom:1rem;display:none;align-items:center;gap:8px}
.alert.show{display:flex}
.alert-ok{background:var(--green-l);color:var(--green);border:1px solid var(--green-m)}
.alert-err{background:var(--red-l);color:var(--red);border:1px solid var(--red-m)}
/* TABLE */
.tbl-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:13.5px}
thead tr{background:var(--g50)}
th{padding:11px 14px;text-align:left;font-size:11px;font-weight:700;color:var(--g400);text-transform:uppercase;letter-spacing:.06em;border-bottom:1px solid var(--g200);white-space:nowrap}
td{padding:13px 14px;border-bottom:1px solid var(--g100);color:var(--g800);vertical-align:middle}
tr:last-child td{border-bottom:none}
tr:hover td{background:var(--g50)}
/* BADGE */
.badge{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600}
.b-hadir{background:var(--green-l);color:var(--green)}
.b-alpha{background:var(--red-l);color:var(--red)}
.b-izin{background:var(--yellow-l);color:var(--yellow)}
.b-sakit{background:var(--blue-l);color:var(--blue)}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.dy{background:var(--yellow)}.db{background:var(--blue)}
/* EMPTY */
.empty{text-align:center;padding:3rem 1rem;color:var(--g400)}
.empty-ico{font-size:40px;margin-bottom:.75rem}
/* API ENDPOINT LIST */
.api-row{display:flex;align-items:center;padding:10px 0;border-bottom:1px solid var(--g100);font-size:13px}
.api-row:last-child{border-bottom:none}
.api-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;margin-right:8px;min-width:42px;text-align:center}
.get{background:#DBEAFE;color:#1D4ED8}.post{background:#D1FAE5;color:#065F46}
.api-path{font-family:monospace;color:var(--g800);font-size:13px}
.api-desc{color:var(--g400);font-size:12px;margin-left:auto;padding-left:12px}
/* HEALTH PAGE */
.health-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:1.5rem}
.health-item{background:var(--g50);border:1px solid var(--g200);border-radius:var(--rs);padding:1.125rem 1.25rem}
.health-item-label{font-size:11px;font-weight:700;color:var(--g400);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.health-item-val{font-size:15px;font-weight:600;color:var(--g800)}
.health-item-val.ok{color:var(--green)}
.pulse{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--green);margin-right:6px;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
/* INFO BOXES */
.info-box{background:var(--blue-l);border:1px solid var(--blue-m);border-radius:var(--rs);padding:1rem 1.25rem;font-size:13px;color:#1E40AF;margin-bottom:1rem;display:flex;gap:10px;align-items:flex-start}
.warn-box{background:var(--yellow-l);border:1px solid var(--yellow-m);border-radius:var(--rs);padding:1rem 1.25rem;font-size:13px;color:#92400E;margin-bottom:1rem;display:flex;gap:10px;align-items:flex-start}
/* MISC */
.mono{font-family:monospace;font-size:13px;color:var(--g600)}
.small{font-size:12px;color:var(--g400)}
.fw600{font-weight:600}
pre.code{background:#1E293B;color:#E2E8F0;border-radius:var(--rs);padding:1rem 1.25rem;font-size:13px;overflow-x:auto;line-height:1.7;margin-top:.75rem}
</style>
"""

NAV = """
<nav>
  <div class="nav-inner">
    <a class="nav-tab {a0}" href="/">🏠 Beranda</a>
    <a class="nav-tab {a1}" href="/kehadiran-page">📋 Kehadiran</a>
    <a class="nav-tab {a2}" href="/kesehatan-page">💚 Kesehatan</a>
  </div>
</nav>
"""

HEADER = """
<header>
  <div class="hdr">
    <div class="hdr-left">
      <div class="hdr-icon">🎓</div>
      <div>
        <div class="hdr-title">Sistem Pencatatan Kehadiran</div>
        <div class="hdr-sub">Platform as a Service · Railway Cloud</div>
      </div>
    </div>
    <div class="hdr-badge">✅ v1.0.0 · Aktif</div>
  </div>
</header>
"""

def make_nav(active):
    a = ['','','']
    a[active] = 'active'
    return NAV.format(a0=a[0], a1=a[1], a2=a[2])

def get_badge(status):
    m = {
        'hadir':  ('b-hadir','dg','✅'),
        'izin':   ('b-izin','dy','📋'),
        'sakit':  ('b-sakit','db','🏥'),
        'alpha':  ('b-alpha','dr','❌'),
    }
    cls, dot, icon = m.get(status, ('b-izin','dy','❓'))
    label = status.capitalize()
    return f'<span class="badge {cls}"><span class="dot {dot}"></span>{icon} {label}</span>'

# ─── PAGE: BERANDA ─────────────────────────────────────────────────────────────
@app.route('/')
def beranda():
    total = Kehadiran.query.count()
    html = f"""<!DOCTYPE html><html lang="id"><head>{BASE_STYLE}<title>Beranda · Kehadiran</title></head><body>
{HEADER}{make_nav(0)}
<div class="main">
  <div class="grid2">
    <div>
      <!-- FORM ABSEN -->
      <div class="card">
        <div class="card-hdr">
          <div class="card-hdr-icon blue">📝</div>
          <div><div class="card-title">Catat Kehadiran</div><div class="card-sub">Isi form untuk absensi</div></div>
        </div>
        <div class="card-body">
          <div class="alert alert-ok" id="ok">✅ Kehadiran berhasil dicatat!</div>
          <div class="alert alert-err" id="err">❌ Gagal mencatat. Periksa kembali.</div>
          <div class="form-group"><label>Nama Lengkap</label><input id="nama" type="text" placeholder="Contoh: Budi Santoso" required></div>
          <div class="form-group"><label>NIM</label><input id="nim" type="text" placeholder="Contoh: 1234567890" required></div>
          <div class="form-group"><label>Tanggal</label><input id="tanggal" type="date" required></div>
          <div class="form-group"><label>Status Kehadiran</label>
            <select id="status">
              <option value="hadir">✅ Hadir</option>
              <option value="izin">📋 Izin</option>
              <option value="sakit">🏥 Sakit</option>
              <option value="alpha">❌ Alpha</option>
            </select>
          </div>
          <button class="btn btn-primary" onclick="kirim()">📤 Kirim Absen</button>
        </div>
      </div>
      <!-- API INFO -->
      <div class="card">
        <div class="card-hdr"><div class="card-hdr-icon teal">🔌</div>
          <div><div class="card-title">Endpoint API</div><div class="card-sub">REST API tersedia</div></div>
        </div>
        <div class="card-body" style="padding:1rem 1.5rem">
          <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran</span><span class="api-desc">Semua data JSON</span></div>
          <div class="api-row"><span class="api-tag post">POST</span><span class="api-path">/kehadiran</span><span class="api-desc">Tambah data</span></div>
          <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran/{{id}}</span><span class="api-desc">Detail per ID</span></div>
          <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kesehatan</span><span class="api-desc">Health check JSON</span></div>
        </div>
      </div>
    </div>
    <!-- TABEL -->
    <div class="card">
      <div class="card-hdr">
        <div class="card-hdr-icon green">📋</div>
        <div><div class="card-title">Daftar Kehadiran</div><div class="card-sub" id="sub">Memuat...</div></div>
      </div>
      <div style="padding:1rem 1.5rem 0">
        <div class="stats">
          <div class="stat hadir"><div class="stat-num" id="sH">0</div><div class="stat-lbl">Hadir</div></div>
          <div class="stat izin"><div class="stat-num" id="sI">0</div><div class="stat-lbl">Izin/Sakit</div></div>
          <div class="stat alpha"><div class="stat-num" id="sA">0</div><div class="stat-lbl">Alpha</div></div>
        </div>
      </div>
      <div class="tbl-wrap">
        <table><thead><tr><th>#</th><th>Nama</th><th>NIM</th><th>Tanggal</th><th>Status</th><th>Waktu Absen</th></tr></thead>
        <tbody id="tbody"><tr><td colspan="6"><div class="empty"><div class="empty-ico">⏳</div><p>Memuat data...</p></div></td></tr></tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<script>
const today = new Date().toISOString().split('T')[0];
document.getElementById('tanggal').value = today;
function fmt(s){{try{{const d=new Date(s);return d.toLocaleString('id-ID',{{day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'}})}}catch{{return s}}}}
function badge(st){{const m={{hadir:['b-hadir','dg','✅'],izin:['b-izin','dy','📋'],sakit:['b-sakit','db','🏥'],alpha:['b-alpha','dr','❌']}};const[c,d,i]=m[st]||m.izin;return`<span class="badge ${{c}}"><span class="dot ${{d}}"></span>${{i}} ${{st.charAt(0).toUpperCase()+st.slice(1)}}</span>`}}
async function load(){{
  const r=await fetch('/kehadiran');const j=await r.json();const data=j.data||[];
  document.getElementById('sub').textContent=data.length+' record ditemukan';
  let h=0,iz=0,a=0;
  data.forEach(d=>{{if(d.status==='hadir')h++;else if(d.status==='alpha')a++;else iz++;}});
  document.getElementById('sH').textContent=h;
  document.getElementById('sI').textContent=iz;
  document.getElementById('sA').textContent=a;
  const tb=document.getElementById('tbody');
  if(!data.length){{tb.innerHTML='<tr><td colspan="6"><div class="empty"><div class="empty-ico">📭</div><p>Belum ada data. Isi form untuk mulai absen.</p></div></td></tr>';return;}}
  tb.innerHTML=data.map(d=>`<tr><td class="small fw600">#${{d.id}}</td><td class="fw600">${{d.nama}}</td><td class="mono">${{d.nim}}</td><td>${{d.tanggal}}</td><td>${{badge(d.status)}}</td><td class="small">${{fmt(d.waktu_absen)}}</td></tr>`).join('');
}}
async function kirim(){{
  const b=document.querySelector('.btn-primary');b.disabled=true;b.textContent='⏳ Mengirim...';
  const body={{nama:document.getElementById('nama').value,nim:document.getElementById('nim').value,tanggal:document.getElementById('tanggal').value,status:document.getElementById('status').value}};
  try{{
    const r=await fetch('/kehadiran',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(body)}});
    if(r.ok){{const el=document.getElementById('ok');el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3000);document.getElementById('nama').value='';document.getElementById('nim').value='';document.getElementById('tanggal').value=today;await load();}}
    else{{const el=document.getElementById('err');el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3000);}}
  }}catch{{const el=document.getElementById('err');el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3000);}}
  b.disabled=false;b.innerHTML='📤 Kirim Absen';
}}
load();setInterval(load,30000);
</script>
</body></html>"""
    return html

# ─── PAGE: KEHADIRAN (visual) ──────────────────────────────────────────────────
@app.route('/kehadiran-page')
def kehadiran_page():
    data = Kehadiran.query.order_by(Kehadiran.waktu_absen.desc()).all()
    total = len(data)
    hadir = sum(1 for k in data if k.status == 'hadir')
    izin  = sum(1 for k in data if k.status in ['izin','sakit'])
    alpha = sum(1 for k in data if k.status == 'alpha')

    rows = ""
    for k in data:
        rows += f"""<tr>
          <td class="small fw600">#{k.id}</td>
          <td class="fw600">{k.nama}</td>
          <td class="mono">{k.nim}</td>
          <td>{k.tanggal}</td>
          <td>{get_badge(k.status)}</td>
          <td class="small">{k.waktu_absen.strftime('%d %b %Y, %H:%M') if k.waktu_absen else '-'}</td>
        </tr>"""

    if not rows:
        rows = '<tr><td colspan="6"><div class="empty"><div class="empty-ico">📭</div><p>Belum ada data kehadiran.</p></div></td></tr>'

    html = f"""<!DOCTYPE html><html lang="id"><head>{BASE_STYLE}<title>Data Kehadiran</title></head><body>
{HEADER}{make_nav(1)}
<div class="main">
  <!-- STATS -->
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem">
    <div class="card" style="margin:0"><div class="card-body" style="text-align:center;padding:1.25rem">
      <div style="font-size:28px;font-weight:700;color:var(--blue)">{total}</div>
      <div class="small" style="margin-top:4px;font-weight:600;text-transform:uppercase;letter-spacing:.04em">Total</div>
    </div></div>
    <div class="card" style="margin:0"><div class="card-body" style="text-align:center;padding:1.25rem">
      <div style="font-size:28px;font-weight:700;color:var(--green)">{hadir}</div>
      <div class="small" style="margin-top:4px;font-weight:600;text-transform:uppercase;letter-spacing:.04em">Hadir</div>
    </div></div>
    <div class="card" style="margin:0"><div class="card-body" style="text-align:center;padding:1.25rem">
      <div style="font-size:28px;font-weight:700;color:var(--yellow)">{izin}</div>
      <div class="small" style="margin-top:4px;font-weight:600;text-transform:uppercase;letter-spacing:.04em">Izin/Sakit</div>
    </div></div>
    <div class="card" style="margin:0"><div class="card-body" style="text-align:center;padding:1.25rem">
      <div style="font-size:28px;font-weight:700;color:var(--red)">{alpha}</div>
      <div class="small" style="margin-top:4px;font-weight:600;text-transform:uppercase;letter-spacing:.04em">Alpha</div>
    </div></div>
  </div>

  <!-- TABEL LENGKAP -->
  <div class="card">
    <div class="card-hdr">
      <div class="card-hdr-icon green">📋</div>
      <div><div class="card-title">Semua Data Kehadiran</div><div class="card-sub">{total} record tersimpan · diperbarui otomatis</div></div>
      <button class="btn btn-primary" style="width:auto;margin-left:auto;padding:8px 16px;font-size:13px" onclick="location.reload()">🔄 Refresh</button>
    </div>
    <div class="tbl-wrap">
      <table><thead><tr><th>#</th><th>Nama</th><th>NIM</th><th>Tanggal</th><th>Status</th><th>Waktu Absen</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>
  </div>

  <!-- API RAW INFO -->
  <div class="card">
    <div class="card-hdr"><div class="card-hdr-icon teal">📡</div>
      <div><div class="card-title">Akses via API (JSON)</div><div class="card-sub">Endpoint REST untuk integrasi sistem</div></div>
    </div>
    <div class="card-body">
      <div class="info-box">💡 Data ini juga tersedia dalam format JSON melalui endpoint <code style="background:rgba(37,99,235,.1);padding:1px 6px;border-radius:4px">/kehadiran</code></div>
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran</span><span class="api-desc">Semua data dalam format JSON</span></div>
      <div class="api-row"><span class="api-tag post">POST</span><span class="api-path">/kehadiran</span><span class="api-desc">Tambah data baru via JSON body</span></div>
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran/{{id}}</span><span class="api-desc">Detail satu record berdasarkan ID</span></div>
      <p style="margin-top:1rem;font-size:13px;color:var(--g500)">Contoh body POST:</p>
      <pre class="code">{{"nama": "Budi Santoso", "nim": "1234567890", "tanggal": "2026-05-11", "status": "hadir"}}</pre>
    </div>
  </div>
</div>
</body></html>"""
    return html

# ─── PAGE: KESEHATAN (visual) ──────────────────────────────────────────────────
@app.route('/kesehatan-page')
def kesehatan_page():
    now = datetime.utcnow()
    total_data = Kehadiran.query.count()
    db_status = "Terhubung"
    try:
        db.session.execute(db.text('SELECT 1'))
    except:
        db_status = "Error"

    html = f"""<!DOCTYPE html><html lang="id"><head>{BASE_STYLE}<title>Status Kesehatan</title></head><body>
{HEADER}{make_nav(2)}
<div class="main">

  <!-- STATUS UTAMA -->
  <div class="card">
    <div class="card-hdr">
      <div class="card-hdr-icon green">💚</div>
      <div><div class="card-title">Status Sistem</div><div class="card-sub">Pemantauan real-time aplikasi</div></div>
    </div>
    <div class="card-body">
      <div style="display:flex;align-items:center;gap:12px;padding:1rem;background:var(--green-l);border:1px solid var(--green-m);border-radius:var(--rs);margin-bottom:1.25rem">
        <span style="font-size:28px">✅</span>
        <div>
          <div style="font-size:16px;font-weight:700;color:var(--green)"><span class="pulse"></span>Semua Sistem Berjalan Normal</div>
          <div class="small" style="margin-top:2px">Aplikasi aktif dan merespons dengan baik</div>
        </div>
      </div>
      <div class="health-grid">
        <div class="health-item">
          <div class="health-item-label">Status Aplikasi</div>
          <div class="health-item-val ok">🟢 Aktif</div>
        </div>
        <div class="health-item">
          <div class="health-item-label">Database</div>
          <div class="health-item-val ok">🟢 {db_status}</div>
        </div>
        <div class="health-item">
          <div class="health-item-label">Versi Aplikasi</div>
          <div class="health-item-val">v1.0.0</div>
        </div>
        <div class="health-item">
          <div class="health-item-label">Platform</div>
          <div class="health-item-val">Railway PaaS</div>
        </div>
        <div class="health-item">
          <div class="health-item-label">Framework</div>
          <div class="health-item-val">Flask 3.x</div>
        </div>
        <div class="health-item">
          <div class="health-item-label">Total Data</div>
          <div class="health-item-val">{total_data} record</div>
        </div>
        <div class="health-item">
          <div class="health-item-label">Server Time (UTC)</div>
          <div class="health-item-val">{now.strftime('%d %b %Y')}</div>
        </div>
        <div class="health-item">
          <div class="health-item-label">Waktu Server</div>
          <div class="health-item-val" id="clock">{now.strftime('%H:%M:%S')}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- INFO PAAS -->
  <div class="card">
    <div class="card-hdr"><div class="card-hdr-icon blue">☁️</div>
      <div><div class="card-title">Informasi Deployment PaaS</div><div class="card-sub">Detail platform dan infrastruktur</div></div>
    </div>
    <div class="card-body">
      <div class="health-grid">
        <div class="health-item"><div class="health-item-label">Cloud Provider</div><div class="health-item-val">Railway</div></div>
        <div class="health-item"><div class="health-item-label">Model Layanan</div><div class="health-item-val">Platform as a Service</div></div>
        <div class="health-item"><div class="health-item-label">Runtime</div><div class="health-item-val">Python 3.13</div></div>
        <div class="health-item"><div class="health-item-label">Web Server</div><div class="health-item-val">Gunicorn</div></div>
        <div class="health-item"><div class="health-item-label">Database</div><div class="health-item-val">SQLite (via SQLAlchemy)</div></div>
        <div class="health-item"><div class="health-item-label">Auto-Deploy</div><div class="health-item-val ok">🟢 Aktif (GitHub)</div></div>
      </div>
    </div>
  </div>

  <!-- ENDPOINT LIST -->
  <div class="card">
    <div class="card-hdr"><div class="card-hdr-icon teal">🔌</div>
      <div><div class="card-title">Semua Endpoint</div><div class="card-sub">Daftar lengkap route aplikasi</div></div>
    </div>
    <div class="card-body" style="padding:1rem 1.5rem">
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/</span><span class="api-desc">Halaman utama + form absen</span></div>
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran-page</span><span class="api-desc">Halaman data kehadiran (visual)</span></div>
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kesehatan-page</span><span class="api-desc">Halaman status kesehatan (visual)</span></div>
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran</span><span class="api-desc">API — semua data JSON</span></div>
      <div class="api-row"><span class="api-tag post">POST</span><span class="api-path">/kehadiran</span><span class="api-desc">API — tambah data baru</span></div>
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran/{{id}}</span><span class="api-desc">API — detail per ID</span></div>
      <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kesehatan</span><span class="api-desc">API — health check JSON</span></div>
    </div>
  </div>

</div>
<script>
setInterval(()=>{{
  const el=document.getElementById('clock');
  if(el){{const n=new Date();el.textContent=n.toUTCString().split(' ')[4];}}
}},1000);
</script>
</body></html>"""
    return html

# ─── API ENDPOINTS (JSON) ──────────────────────────────────────────────────────
@app.route('/kesehatan')
def cek_kesehatan():
    try:
        db.session.execute(db.text('SELECT 1'))
        db_ok = True
    except:
        db_ok = False
    return jsonify({
        'status': 'sehat',
        'waktu': str(datetime.utcnow()),
        'versi': '1.0.0',
        'database': 'terhubung' if db_ok else 'error',
        'platform': 'Railway PaaS',
        'total_data': Kehadiran.query.count()
    })

@app.route('/kehadiran', methods=['GET'])
def daftar_kehadiran():
    data = Kehadiran.query.order_by(Kehadiran.waktu_absen.desc()).all()
    hasil = [{'id':k.id,'nama':k.nama,'nim':k.nim,'tanggal':k.tanggal,'status':k.status,'waktu_absen':str(k.waktu_absen)} for k in data]
    return jsonify({'total': len(hasil), 'data': hasil})

@app.route('/kehadiran', methods=['POST'])
def tambah_kehadiran():
    body = request.get_json()
    if not body or not all(k in body for k in ['nama','nim','tanggal','status']):
        return jsonify({'error': 'Field nama, nim, tanggal, status wajib diisi'}), 400
    baru = Kehadiran(nama=body['nama'], nim=body['nim'], tanggal=body['tanggal'], status=body['status'])
    db.session.add(baru)
    db.session.commit()
    return jsonify({'pesan': 'Kehadiran berhasil dicatat', 'id': baru.id}), 201

@app.route('/kehadiran/<int:id>', methods=['GET'])
def detail_kehadiran(id):
    k = Kehadiran.query.get_or_404(id)
    return jsonify({'id':k.id,'nama':k.nama,'nim':k.nim,'tanggal':k.tanggal,'status':k.status,'waktu_absen':str(k.waktu_absen)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)