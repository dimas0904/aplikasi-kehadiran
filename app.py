from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///kehadiran.db'
)
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

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sistem Pencatatan Kehadiran Mahasiswa</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --blue: #2563EB; --blue-light: #EFF6FF; --blue-mid: #BFDBFE;
    --green: #16A34A; --green-light: #F0FDF4; --green-mid: #BBF7D0;
    --red: #DC2626; --red-light: #FEF2F2; --red-mid: #FECACA;
    --yellow: #D97706; --yellow-light: #FFFBEB; --yellow-mid: #FDE68A;
    --gray-50: #F9FAFB; --gray-100: #F3F4F6; --gray-200: #E5E7EB;
    --gray-400: #9CA3AF; --gray-600: #4B5563; --gray-800: #1F2937; --gray-900: #111827;
    --radius: 12px; --radius-sm: 8px; --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
  }
  body { font-family: 'Plus Jakarta Sans', sans-serif; background: #F1F5F9; color: var(--gray-900); min-height: 100vh; }
  header {
    background: linear-gradient(135deg, #1E40AF 0%, #2563EB 50%, #3B82F6 100%);
    color: white; padding: 0; position: sticky; top: 0; z-index: 100;
    box-shadow: 0 2px 12px rgba(37,99,235,0.3);
  }
  .header-inner { max-width: 1100px; margin: 0 auto; padding: 1rem 1.5rem; display: flex; align-items: center; justify-content: space-between; }
  .header-left { display: flex; align-items: center; gap: 12px; }
  .header-icon { width: 40px; height: 40px; background: rgba(255,255,255,0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
  .header-title { font-size: 17px; font-weight: 700; }
  .header-sub { font-size: 12px; opacity: 0.8; margin-top: 1px; }
  .header-badge { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 999px; padding: 4px 12px; font-size: 12px; font-weight: 500; }
  .main { max-width: 1100px; margin: 0 auto; padding: 1.5rem; display: grid; grid-template-columns: 380px 1fr; gap: 1.5rem; align-items: start; }
  @media (max-width: 800px) { .main { grid-template-columns: 1fr; } }
  .card { background: white; border-radius: var(--radius); box-shadow: var(--shadow); border: 1px solid var(--gray-200); overflow: hidden; }
  .card-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--gray-100); display: flex; align-items: center; gap: 10px; }
  .card-header-icon { width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
  .card-header-icon.blue { background: var(--blue-light); }
  .card-header-icon.green { background: var(--green-light); }
  .card-title { font-size: 15px; font-weight: 600; color: var(--gray-800); }
  .card-sub { font-size: 12px; color: var(--gray-400); margin-top: 1px; }
  .card-body { padding: 1.5rem; }
  .stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.5rem; }
  .stat { background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius-sm); padding: 0.875rem; text-align: center; }
  .stat-num { font-size: 22px; font-weight: 700; line-height: 1; }
  .stat-label { font-size: 11px; color: var(--gray-400); margin-top: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
  .stat.hadir .stat-num { color: var(--green); }
  .stat.alpha .stat-num { color: var(--red); }
  .stat.izin .stat-num { color: var(--yellow); }
  form { display: flex; flex-direction: column; gap: 1rem; }
  .form-group { display: flex; flex-direction: column; gap: 6px; }
  label { font-size: 13px; font-weight: 600; color: var(--gray-600); }
  input, select {
    padding: 10px 14px; border: 1.5px solid var(--gray-200); border-radius: var(--radius-sm);
    font-size: 14px; font-family: inherit; color: var(--gray-900); background: var(--gray-50);
    transition: all 0.15s; outline: none;
  }
  input:focus, select:focus { border-color: var(--blue); background: white; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
  select { cursor: pointer; }
  .btn { padding: 11px 20px; border: none; border-radius: var(--radius-sm); font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.15s; font-family: inherit; display: flex; align-items: center; justify-content: center; gap: 8px; }
  .btn-primary { background: var(--blue); color: white; width: 100%; }
  .btn-primary:hover { background: #1D4ED8; transform: translateY(-1px); box-shadow: var(--shadow-md); }
  .btn-primary:active { transform: translateY(0); }
  .alert { padding: 12px 16px; border-radius: var(--radius-sm); font-size: 13px; font-weight: 500; margin-bottom: 1rem; display: none; align-items: center; gap: 8px; }
  .alert.show { display: flex; }
  .alert-success { background: var(--green-light); color: var(--green); border: 1px solid var(--green-mid); }
  .alert-error { background: var(--red-light); color: var(--red); border: 1px solid var(--red-mid); }
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
  thead tr { background: var(--gray-50); }
  th { padding: 11px 14px; text-align: left; font-size: 11px; font-weight: 700; color: var(--gray-400); text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid var(--gray-200); white-space: nowrap; }
  td { padding: 13px 14px; border-bottom: 1px solid var(--gray-100); color: var(--gray-800); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--gray-50); }
  .badge { display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
  .badge-hadir { background: var(--green-light); color: var(--green); }
  .badge-alpha { background: var(--red-light); color: var(--red); }
  .badge-izin { background: var(--yellow-light); color: var(--yellow); }
  .badge-sakit { background: #EFF6FF; color: #2563EB; }
  .empty-state { text-align: center; padding: 3rem 1rem; color: var(--gray-400); }
  .empty-state-icon { font-size: 40px; margin-bottom: 0.75rem; }
  .empty-state p { font-size: 14px; }
  .nim-text { font-family: monospace; font-size: 13px; color: var(--gray-600); }
  .id-text { font-size: 12px; color: var(--gray-400); font-weight: 600; }
  .time-text { font-size: 12px; color: var(--gray-400); }
  .dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
  .dot-green { background: var(--green); }
  .dot-red { background: var(--red); }
  .dot-yellow { background: var(--yellow); }
  .dot-blue { background: var(--blue); }
  .api-section { margin-top: 1.5rem; }
  .api-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; margin-right: 6px; }
  .get { background: #DBEAFE; color: #1D4ED8; }
  .post { background: #D1FAE5; color: #065F46; }
  .api-row { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--gray-100); font-size: 13px; }
  .api-row:last-child { border-bottom: none; }
  .api-path { font-family: monospace; color: var(--gray-800); font-size: 12.5px; }
  .api-desc { color: var(--gray-400); font-size: 12px; margin-left: auto; }
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="header-left">
      <div class="header-icon">🎓</div>
      <div>
        <div class="header-title">Sistem Pencatatan Kehadiran</div>
        <div class="header-sub">Platform as a Service · Railway Cloud</div>
      </div>
    </div>
    <div class="header-badge">✅ v1.0.0 · Aktif</div>
  </div>
</header>

<div class="main">
  <!-- KOLOM KIRI: Form -->
  <div style="display: flex; flex-direction: column; gap: 1.5rem;">

    <!-- Stats -->
    <div class="card">
      <div class="card-body" style="padding: 1.25rem;">
        <div class="stats-row" id="statsRow">
          <div class="stat hadir"><div class="stat-num" id="statHadir">0</div><div class="stat-label">Hadir</div></div>
          <div class="stat izin"><div class="stat-num" id="statIzin">0</div><div class="stat-label">Izin/Sakit</div></div>
          <div class="stat alpha"><div class="stat-num" id="statAlpha">0</div><div class="stat-label">Alpha</div></div>
        </div>
      </div>
    </div>

    <!-- Form Absen -->
    <div class="card">
      <div class="card-header">
        <div class="card-header-icon blue">📝</div>
        <div>
          <div class="card-title">Catat Kehadiran</div>
          <div class="card-sub">Isi form di bawah untuk absen</div>
        </div>
      </div>
      <div class="card-body">
        <div class="alert alert-success" id="alertSuccess">✅ Kehadiran berhasil dicatat!</div>
        <div class="alert alert-error" id="alertError">❌ Gagal mencatat kehadiran.</div>
        <form id="formAbsen">
          <div class="form-group">
            <label>Nama Lengkap</label>
            <input type="text" id="nama" placeholder="Contoh: Budi Santoso" required>
          </div>
          <div class="form-group">
            <label>NIM</label>
            <input type="text" id="nim" placeholder="Contoh: 1234567890" required>
          </div>
          <div class="form-group">
            <label>Tanggal</label>
            <input type="date" id="tanggal" required>
          </div>
          <div class="form-group">
            <label>Status Kehadiran</label>
            <select id="status">
              <option value="hadir">✅ Hadir</option>
              <option value="izin">📋 Izin</option>
              <option value="sakit">🏥 Sakit</option>
              <option value="alpha">❌ Alpha</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">
            <span>📤</span> Kirim Absen
          </button>
        </form>
      </div>
    </div>

    <!-- Info API -->
    <div class="card">
      <div class="card-header">
        <div class="card-header-icon blue">🔌</div>
        <div>
          <div class="card-title">Endpoint API</div>
          <div class="card-sub">REST API tersedia</div>
        </div>
      </div>
      <div class="card-body" style="padding: 1rem 1.5rem;">
        <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran</span><span class="api-desc">Semua data</span></div>
        <div class="api-row"><span class="api-tag post">POST</span><span class="api-path">/kehadiran</span><span class="api-desc">Tambah data</span></div>
        <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kehadiran/{id}</span><span class="api-desc">Detail data</span></div>
        <div class="api-row"><span class="api-tag get">GET</span><span class="api-path">/kesehatan</span><span class="api-desc">Health check</span></div>
      </div>
    </div>

  </div>

  <!-- KOLOM KANAN: Tabel -->
  <div class="card">
    <div class="card-header">
      <div class="card-header-icon green">📋</div>
      <div>
        <div class="card-title">Daftar Kehadiran</div>
        <div class="card-sub" id="tableSubtitle">Memuat data...</div>
      </div>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Nama</th>
            <th>NIM</th>
            <th>Tanggal</th>
            <th>Status</th>
            <th>Waktu Absen</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          <tr><td colspan="6"><div class="empty-state"><div class="empty-state-icon">⏳</div><p>Memuat data...</p></div></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
const today = new Date().toISOString().split('T')[0];
document.getElementById('tanggal').value = today;

function getBadge(status) {
  const map = {
    hadir: ['badge-hadir','dot-green','✅'],
    izin:  ['badge-izin','dot-yellow','📋'],
    sakit: ['badge-sakit','dot-blue','🏥'],
    alpha: ['badge-alpha','dot-red','❌']
  };
  const [cls, dot, icon] = map[status] || ['badge-izin','dot-yellow','❓'];
  return `<span class="badge ${cls}"><span class="dot ${dot}"></span>${icon} ${status.charAt(0).toUpperCase()+status.slice(1)}</span>`;
}

function formatWaktu(str) {
  try {
    const d = new Date(str);
    return d.toLocaleString('id-ID', {day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'});
  } catch { return str; }
}

async function loadData() {
  try {
    const res = await fetch('/kehadiran');
    const json = await res.json();
    const data = json.data || [];
    const tbody = document.getElementById('tableBody');
    const subtitle = document.getElementById('tableSubtitle');
    subtitle.textContent = `${data.length} record ditemukan`;

    let hadir=0, izin=0, alpha=0;
    data.forEach(d => {
      if (d.status==='hadir') hadir++;
      else if (d.status==='alpha') alpha++;
      else izin++;
    });
    document.getElementById('statHadir').textContent = hadir;
    document.getElementById('statIzin').textContent = izin;
    document.getElementById('statAlpha').textContent = alpha;

    if (data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6"><div class="empty-state"><div class="empty-state-icon">📭</div><p>Belum ada data kehadiran.<br>Isi form di sebelah kiri untuk mulai absen.</p></div></td></tr>`;
      return;
    }
    tbody.innerHTML = data.map(d => `
      <tr>
        <td><span class="id-text">#${d.id}</span></td>
        <td><strong>${d.nama}</strong></td>
        <td><span class="nim-text">${d.nim}</span></td>
        <td>${d.tanggal}</td>
        <td>${getBadge(d.status)}</td>
        <td><span class="time-text">${formatWaktu(d.waktu_absen)}</span></td>
      </tr>`).join('');
  } catch(e) {
    document.getElementById('tableBody').innerHTML = `<tr><td colspan="6"><div class="empty-state"><div class="empty-state-icon">⚠️</div><p>Gagal memuat data.</p></div></td></tr>`;
  }
}

document.getElementById('formAbsen').addEventListener('submit', async function(e) {
  e.preventDefault();
  const btn = this.querySelector('button');
  btn.disabled = true; btn.textContent = '⏳ Mengirim...';
  const body = {
    nama: document.getElementById('nama').value,
    nim: document.getElementById('nim').value,
    tanggal: document.getElementById('tanggal').value,
    status: document.getElementById('status').value
  };
  try {
    const res = await fetch('/kehadiran', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(body)
    });
    if (res.ok) {
      const s = document.getElementById('alertSuccess');
      s.classList.add('show');
      setTimeout(() => s.classList.remove('show'), 3000);
      this.reset();
      document.getElementById('tanggal').value = today;
      await loadData();
    } else {
      document.getElementById('alertError').classList.add('show');
      setTimeout(() => document.getElementById('alertError').classList.remove('show'), 3000);
    }
  } catch {
    document.getElementById('alertError').classList.add('show');
    setTimeout(() => document.getElementById('alertError').classList.remove('show'), 3000);
  }
  btn.disabled = false; btn.innerHTML = '<span>📤</span> Kirim Absen';
});

loadData();
setInterval(loadData, 30000);
</script>
</body>
</html>
'''

@app.route('/')
def beranda():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api')
def api_info():
    return jsonify({
        'pesan': 'Aplikasi Pencatatan Kehadiran Mahasiswa',
        'status': 'aktif',
        'versi': '1.0.0',
        'endpoints': ['/kehadiran', '/kehadiran/{id}', '/kesehatan']
    })

@app.route('/kesehatan')
def cek_kesehatan():
    return jsonify({'status': 'sehat', 'waktu': str(datetime.utcnow())})

@app.route('/kehadiran', methods=['GET'])
def daftar_kehadiran():
    data = Kehadiran.query.order_by(Kehadiran.waktu_absen.desc()).all()
    hasil = [{
        'id': k.id, 'nama': k.nama, 'nim': k.nim,
        'tanggal': k.tanggal, 'status': k.status,
        'waktu_absen': str(k.waktu_absen)
    } for k in data]
    return jsonify({'total': len(hasil), 'data': hasil})

@app.route('/kehadiran', methods=['POST'])
def tambah_kehadiran():
    body = request.get_json()
    if not body or not all(k in body for k in ['nama','nim','tanggal','status']):
        return jsonify({'error': 'Field nama, nim, tanggal, status wajib diisi'}), 400
    baru = Kehadiran(
        nama=body['nama'], nim=body['nim'],
        tanggal=body['tanggal'], status=body['status']
    )
    db.session.add(baru)
    db.session.commit()
    return jsonify({'pesan': 'Kehadiran berhasil dicatat', 'id': baru.id}), 201

@app.route('/kehadiran/<int:id>', methods=['GET'])
def detail_kehadiran(id):
    k = Kehadiran.query.get_or_404(id)
    return jsonify({
        'id': k.id, 'nama': k.nama, 'nim': k.nim,
        'tanggal': k.tanggal, 'status': k.status,
        'waktu_absen': str(k.waktu_absen)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)