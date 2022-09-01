(function(){
    const btnexcluir = document.querySelectorAll(".btnExcluir");

btnexcluir.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        const confirmacao = confirm("Deseja realmente excluir esta pessoa?");
        if(!confirmacao){
            e.preventDefault();
        }
    });
});
    
})();