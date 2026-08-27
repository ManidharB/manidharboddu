const header=document.getElementById('siteHeader');
const progress=document.getElementById('progressBar');
const menuToggle=document.getElementById('menuToggle');
const mainNav=document.getElementById('mainNav');

function onScroll(){
  const y=window.scrollY;
  header.classList.toggle('scrolled',y>12);
  const h=document.documentElement.scrollHeight-window.innerHeight;
  progress.style.width=(h>0?Math.min(100,(y/h)*100):0)+'%';
}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();

menuToggle?.addEventListener('click',()=>{
  const open=mainNav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded',String(open));
});
mainNav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
  mainNav.classList.remove('open');menuToggle?.setAttribute('aria-expanded','false');
}));

const revealObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');revealObserver.unobserve(entry.target)}})
},{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>revealObserver.observe(el));

const sections=[...document.querySelectorAll('main section[id]')];
const navLinks=[...document.querySelectorAll('.main-nav a')];
const sectionObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      navLinks.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+entry.target.id));
    }
  })
},{rootMargin:'-42% 0px -50% 0px',threshold:0});
sections.forEach(s=>sectionObserver.observe(s));
