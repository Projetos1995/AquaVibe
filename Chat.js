// AquaVibe — Chat da comunidade (Firebase Firestore + Auth anônimo)
// Uso: <script type="module" src="chat.js"></script> antes de </body> no index.html
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, signInAnonymously } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, collection, addDoc, deleteDoc, doc, getDoc, query, orderBy, limit, onSnapshot, serverTimestamp }
  from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// 1) COLE AQUI a config do seu projeto Firebase (Configurações do projeto > Seus apps)
const firebaseConfig = {
  apiKey: "COLE_AQUI", authDomain: "COLE_AQUI", projectId: "COLE_AQUI", appId: "COLE_AQUI"
};

// ===== FILTRO DE OFENSAS =====
const LEET = { '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a', '$': 's' };
const norm = s => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .replace(/[013457@$]/g, c => LEET[c]).replace(/(.)\1+/g, '$1');
const BASE = ['porra', 'caralho', 'puta', 'puto', 'merda', 'foda', 'foder', 'fodase', 'buceta', 'cu', 'cuzao',
  'viado', 'arrombado', 'babaca', 'idiota', 'imbecil', 'otario', 'corno', 'desgraca', 'desgracado', 'vagabundo',
  'piranha', 'retardado', 'cacete', 'bosta', 'escroto', 'fdp', 'pqp', 'vsf', 'tnc', 'lixo', 'nojento', 'macaco',
  'preto', 'bicha', 'gordo', 'feio'];
const LISTA = BASE.map(norm);
function tokens(s) { // junta letras soltas: "p u t a" -> "puta"
  const t = norm(s).split(/[^a-z]+/).filter(Boolean), o = []; let r = '';
  for (const x of t) { if (x.length === 1) r += x; else { if (r) { o.push(r); r = ''; } o.push(x); } }
  if (r) o.push(r); return o;
}
const ofensivo = txt => tokens(txt).some(t => LISTA.some(w => t === w || (w.length >= 6 && t.startsWith(w))));

// ===== FIREBASE =====
const app = initializeApp(firebaseConfig), auth = getAuth(app), db = getFirestore(app);
let iniciado = false, uid = null, ehAdmin = false, ultimo = 0;

function montarUI() {
  const grade = document.querySelector('#menu-principal .grade');
  const card = document.createElement('div');
  card.className = 'card-funcao';
  card.innerHTML = '<div class="icone">💬</div><h3>Chat</h3><p>Comunidade</p>';
  card.tabIndex = 0; card.setAttribute('role', 'button');
  card.onclick = () => { mostrarSubTela('sub-chat'); iniciarChat(); };
  card.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); card.click(); } };