$(document).ready(function () {
    $('#appBar').kendoAppBar({
        positionMode: "sticky",
        position: "top",
        items: [
            { template: '<h1 class="links">Rota 12</h1>', type: "contentItem" },
            { type: "spacer" },
            { template: '<button id="BtnRegistrar">Registrar</button>', type: "contentItem"},
            { type: "spacer", width: 1},
            { template: '<button id="BtnEntrar" class="k-primary">Entrar</button>', type: "contentItem"},
        ]
    });

    $('#BtnRegistrar').kendoButton();
    $('#BtnEntrar').kendoButton();
});