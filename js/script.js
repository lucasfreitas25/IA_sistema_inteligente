function toggleGraph() {
    var graph = document.getElementById("graph");
    if (graph.style.display === "none") {
        graph.style.display = "block";
    } else {
        graph.style.display = "none";
    }
}

function limparFormulario() {
    document.getElementById("previsao").reset();
   
}