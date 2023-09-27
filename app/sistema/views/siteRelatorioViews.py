from sistema.models import Alocacao, PropostaProjeto
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO

@login_required(login_url="/auth-user/login-user")
def relatorioHorasTrabalhadasProfessores(request):
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    # Query for the relevant Alocacao records
    alocacoes = Alocacao.objects.filter(
        membroExecucao__isnull=False,
        funcao__icontains="profe",
        atividade__data_realizacao_inicio__gte=data_inicio,
        atividade__data_realizacao_fim__lte=data_fim,
        atividade__proposta_projeto__status=PropostaProjeto.STATUS_APROVADA,
    )

    # Aggregate total cargaHoraria for each unique Pessoa
    carga_horaria_totals = {}
    for alocacao in alocacoes:
        pessoa = alocacao.membroExecucao.pessoa
        carga_horaria_totals[pessoa] = carga_horaria_totals.get(pessoa, 0) + alocacao.cargaHoraria

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Define the headers
    headers = ['nome', 'cpf', 'numero matricula', 'carga horaria total']

    # Write the headers to the worksheet
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Populate the worksheet with aggregated data
    for row_num, (pessoa, total_carga_horaria) in enumerate(carga_horaria_totals.items(), start=1):
        worksheet.write(row_num, 0, pessoa.nome)
        worksheet.write(row_num, 1, pessoa.cpf)
        worksheet.write(row_num, 2, pessoa.numero_matricula)
        worksheet.write(row_num, 3, total_carga_horaria)

    workbook.close()

    response = HttpResponse(output.getvalue(), content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=RelatorioHorasTrabalhadasProfessores.xlsx"
    return response

