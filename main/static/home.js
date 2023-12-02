let nav = document.querySelector('nav')
window.onscroll=function(){ //window.onscroll=()=>{ possible like this
    if(window.scrollY > 30){
        nav.classList.add('sticky')
    }
    else{
        nav.classList.remove('sticky')
    }
}