const views=[...document.querySelectorAll('.view')];
document.querySelectorAll('.nav').forEach(b=>b.onclick=()=>show(b.dataset.target));
function show(id){views.forEach(v=>v.classList.toggle('active',v.id===id));document.querySelectorAll('.nav').forEach(n=>n.classList.toggle('active',n.dataset.target===id));if(id==='history')loadHistory()}
async function scan(){
 const status=document.getElementById('status'); status.textContent='Analyzing…';
 try{
  const res=await fetch('/api/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('email').value,phone:document.getElementById('phone').value})});
  const d=await res.json(); if(!res.ok) throw new Error(d.error||'Scan failed');
  document.getElementById('reportScore').textContent=d.score;
  document.getElementById('bar').style.width=d.score+'%';
  document.getElementById('rEmail').textContent=d.email_findings;
  document.getElementById('rPhone').textContent=d.phone_findings;
  document.getElementById('rBreach').textContent=d.breach_findings;
  document.getElementById('rRisk').textContent=d.ml.risk+' ('+Math.round(d.ml.probability*100)+'%)';
  document.getElementById('mlText').textContent='ML risk assessment: '+d.ml.risk+'. '+d.disclaimer;
  document.getElementById('dashScore').textContent=d.score;
  document.getElementById('dashEmail').textContent=d.email_findings;
  document.getElementById('dashPhone').textContent=d.phone_findings;
  document.getElementById('dashBreach').textContent=d.breach_findings;
  document.getElementById('recommendations').innerHTML=d.recommendations.map(x=>'<div class="rec">✓ '+x+'</div>').join('');
  status.textContent='Analysis completed.';
 }catch(e){status.textContent=e.message}
}
async function checkPermissions(){
 const permissions=[...document.querySelectorAll('.permission-form input:checked')].map(x=>x.value);
 const r=await fetch('/api/permissions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({permissions})});
 const d=await r.json();document.getElementById('permResult').textContent='Risk: '+d.risk+' — '+d.message+' Score points: '+d.points;
}
async function loadHistory(){
 const r=await fetch('/api/history'); const rows=await r.json();
 const el=document.getElementById('historyTable');
 el.innerHTML='<div class="history-row"><b>Score</b><b>Risk</b><b>Findings</b><b>Date</b></div>'+
 rows.map(x=>`<div class="history-row"><span>${x.score}</span><span>${x.risk}</span><span>${x.email_findings+x.phone_findings+x.breach_findings}</span><span>${x.created_at}</span></div>`).join('') || '<p>No scans yet.</p>';
}
new Chart(document.getElementById('chart'),{type:'line',data:{labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],datasets:[{data:[8,10,7,13,11,9,12],tension:.4,fill:true,borderWidth:2}]},options:{plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:'#1a2c35'},beginAtZero:true}}}});
