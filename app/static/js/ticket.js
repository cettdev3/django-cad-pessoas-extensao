function updateTicket(ticket_id, model) {
    console.log("dentro do arquivo estatico: " + ticket_id + " " + model);
    $.ajax({
        url: "/ticketModalEdit/"+ticket_id,
        data: { 
            model: model,
            layout: 6 
        },
        success: function (data) {
            $("#" + "modalTicketContainer").html(data);
            $('#' + "cadastrarTicketModal").modal('toggle');
        }
    });
}
