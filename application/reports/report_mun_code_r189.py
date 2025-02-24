import pandas as pd
from io import BytesIO
from datetime import datetime
from auth.auth import SharePointAuth

class DivergenceReportMUNCODER189:
    """
    Classe responsável por verificar divergências entre os arquivos consolidados de códigos municipais e R189.
    """
    
    def __init__(self):
        self.sharepoint_auth = SharePointAuth()
        
        # Mapeamento de serviços para material e tipo
        self.service_mapping = {
            "14.02": {"material": "80001098", "type": "Assistência Técnica"},
            "17.01": {"material": "80001110", "type": "Acessoria ou Consultoria"},
            "14.01": {"material": "80001097", "type": "LUBRIFICACAO, LIMPEZA"},
            "1.07": {"material": "80001019", "type": "SUPORTE TECNICO EM INFORMATICA"},
            "3115": {"material": "80001110", "type": "Assessoria E Consultoria"},
            "1880": {"material": "80001098", "type": "Assistência Técnica - Instalação"},
            "1.03": {"material": "80001680", "type": "Processamento e Armazenamento"}
        }
        
        self.service_cnpj_mapping = {
            "14.02 - Assistência Técnica": {
                "14.759.173/0002-83", "07.175.725/0042-38", "07.175.725/0014-84",
                "60.621.141/0005-87", "13.772.125/0007-77", "07.175.725/0030-02",
                "60.621.141/0004-04", "07.175.725/0004-02", "07.175.725/0010-50",
                "10.885.321/0001-74", "60.621.141/0006-68", "14.759.173/0001-00",
                "07.175.725/0024-56", "07.175.725/0021-03", "07.175.725/0026-18",
                "84.584.994/0007-16"
            },
            "17.01 - Acessoria ou Consultoria": {
                "14.759.173/0002-83", "07.175.725/0042-38", "07.175.725/0014-84",
                "60.621.141/0005-87", "13.772.125/0007-77", "07.175.725/0030-02",
                "60.621.141/0004-04", "07.175.725/0004-02", "07.175.725/0010-50",
                "10.885.321/0001-74", "60.621.141/0006-68", "14.759.173/0001-00",
                "07.175.725/0024-56", "07.175.725/0021-03", "07.175.725/0026-18",
                "84.584.994/0007-16"
            },
            "14.01 - LUBRIFICACAO, LIMPEZA": {
                "14.759.173/0002-83", "07.175.725/0042-38", "07.175.725/0014-84",
                "60.621.141/0005-87", "13.772.125/0007-77", "07.175.725/0030-02",
                "60.621.141/0004-04", "07.175.725/0004-02", "07.175.725/0010-50",
                "10.885.321/0001-74", "60.621.141/0006-68", "14.759.173/0001-00",
                "07.175.725/0024-56", "07.175.725/0021-03", "07.175.725/0026-18",
                "84.584.994/0007-16"
            },
            "1.07 - SUPORTE TECNICO EM INFORMATICA": {
                "14.759.173/0002-83", "07.175.725/0042-38", "07.175.725/0014-84",
                "60.621.141/0005-87", "13.772.125/0007-77", "07.175.725/0030-02",
                "60.621.141/0004-04", "07.175.725/0004-02", "07.175.725/0010-50",
                "10.885.321/0001-74", "60.621.141/0006-68", "14.759.173/0001-00",
                "07.175.725/0024-56", "07.175.725/0021-03", "07.175.725/0026-18",
                "84.584.994/0007-16"
            },
            "3115 - Assessoria E Consultoria": {
                "14.759.173/0002-83", "07.175.725/0042-38", "07.175.725/0014-84",
                "60.621.141/0005-87", "13.772.125/0007-77", "07.175.725/0030-02",
                "60.621.141/0004-04", "07.175.725/0004-02", "07.175.725/0010-50",
                "10.885.321/0001-74", "60.621.141/0006-68", "14.759.173/0001-00",
                "07.175.725/0024-56", "07.175.725/0021-03", "07.175.725/0026-18",
                "84.584.994/0007-16"
            },
            "1880 - Assistência Técnica - Instalação": {
                "14.759.173/0002-83", "07.175.725/0042-38", "07.175.725/0014-84",
                "60.621.141/0005-87", "13.772.125/0007-77", "07.175.725/0030-02",
                "60.621.141/0004-04", "07.175.725/0004-02", "07.175.725/0010-50",
                "10.885.321/0001-74", "60.621.141/0006-68", "14.759.173/0001-00",
                "07.175.725/0024-56", "07.175.725/0021-03", "07.175.725/0026-18",
                "84.584.994/0007-16"
            },
            "1.03 - Processamento e Armazenamento": {
                "14.759.173/0002-83", "07.175.725/0042-38", "07.175.725/0014-84",
                "60.621.141/0005-87", "13.772.125/0007-77", "07.175.725/0030-02",
                "60.621.141/0004-04", "07.175.725/0004-02", "07.175.725/0010-50",
                "10.885.321/0001-74", "60.621.141/0006-68", "14.759.173/0001-00",
                "07.175.725/0024-56", "07.175.725/0021-03", "07.175.725/0026-18",
                "84.584.994/0007-16"
            }
        }
        
        # Lista de possíveis nomes para a coluna de total
        self.colunas_total = ['Total Geral', 'Grand Total', 'Total Gera', 'Total', 'Valor Total']

    def validate_service_cnpj(self, row) -> bool:
        """
        Valida se o CNPJ está autorizado para o serviço específico.
        
        Args:
            row: Linha do DataFrame contendo Municipality Code e CNPJ - WEG
            
        Returns:
            bool: True se o CNPJ está autorizado para o serviço, False caso contrário
        """
        # Converte o código do município para inteiro
        try:
            municipality_code = str(int(float(str(row['Municipality Code']).strip())))
        except (ValueError, TypeError):
            municipality_code = str(row['Municipality Code']).strip()
            
        cnpj = str(row['CNPJ - WEG']).strip()
        
        # Debug: imprime os valores para verificação
        print(f"Validando: Municipality Code={municipality_code}, CNPJ={cnpj}")
        
        # Procura o serviço que corresponde ao código municipal
        service = None
        for service_name in self.service_cnpj_mapping:
            # Extrai apenas o código numérico do nome do serviço e converte para inteiro
            try:
                service_code = str(int(float(service_name.split(' - ')[0].strip())))
            except (ValueError, TypeError):
                service_code = service_name.split(' - ')[0].strip()
                
            print(f"Comparando: {service_code} == {municipality_code}")
            if service_code == municipality_code:
                service = service_name
                print(f"Serviço encontrado: {service}")
                break
        
        if not service:
            print(f"Nenhum serviço encontrado para o código {municipality_code}")
            return False
        
        is_authorized = cnpj in self.service_cnpj_mapping[service]
        print(f"CNPJ {cnpj} {'está' if is_authorized else 'não está'} autorizado para o serviço {service}")
        return is_authorized

    def check_divergences(self, mun_code_data: pd.DataFrame, r189_data: pd.DataFrame) -> tuple[bool, str, pd.DataFrame, pd.DataFrame]:
        """
        Verifica divergências entre os dados consolidados dos códigos municipais e R189.
        
        Args:
            mun_code_data: DataFrame com os dados consolidados dos códigos municipais
            r189_data: DataFrame com os dados consolidados do R189
            
        Returns:
            tuple contendo:
            - bool: True se houver divergências, False caso contrário
            - str: Mensagem descritiva do resultado
            - DataFrame: DataFrame com as divergências encontradas
            - DataFrame: DataFrame com os dados agrupados
        """
        try:
            # Baixa os arquivos consolidados necessários para obter os números das notas fiscais
            qpe_consolidado = self.sharepoint_auth.baixar_arquivo_sharepoint(
                'QPE_consolidado.xlsx',
                '/teams/BR-TI-TIN/AutomaoFinanas/CONSOLIDADO'
            )
            
            spb_consolidado = self.sharepoint_auth.baixar_arquivo_sharepoint(
                'SPB_consolidado.xlsx',
                '/teams/BR-TI-TIN/AutomaoFinanas/CONSOLIDADO'
            )
            
            # Lê os arquivos consolidados
            qpe_data = pd.read_excel(qpe_consolidado) if qpe_consolidado else pd.DataFrame()
            spb_data = pd.read_excel(spb_consolidado) if spb_consolidado else pd.DataFrame()
            
            # Verifica qual coluna de total está presente no DataFrame
            coluna_total = None
            for col in self.colunas_total:
                if col in mun_code_data.columns:
                    coluna_total = col
                    break
                    
            if not coluna_total:
                raise ValueError(f"Nenhuma coluna de total encontrada. Colunas disponíveis: {', '.join(self.colunas_total)}")

            # Primeiro, valida os CNPJs por serviço
            mun_code_data['CNPJ_Autorizado'] = mun_code_data.apply(self.validate_service_cnpj, axis=1)
            
            # Filtra apenas os registros com CNPJs não autorizados
            cnpj_divergences = mun_code_data[~mun_code_data['CNPJ_Autorizado']].copy()
            cnpj_divergences['Tipo_Divergencia'] = 'CNPJ não autorizado para o serviço'
            
            # Filtra apenas os registros com CNPJs autorizados para o agrupamento
            valid_data = mun_code_data[mun_code_data['CNPJ_Autorizado']].drop('CNPJ_Autorizado', axis=1)
            
            # Agrupa os dados por Municipality Code, CNPJ - WEG e Invoice number
            grouped_data = valid_data.groupby(
                ['Municipality Code', 'CNPJ - WEG', 'Invoice number']
            ).agg({
                coluna_total: 'sum',
                'Site Name - WEG 2': 'first'  # Mantém o primeiro Site Name encontrado
            }).reset_index()
            
            # Ordena o DataFrame agrupado para melhor visualização
            grouped_data = grouped_data.sort_values(
                by=['Municipality Code', 'CNPJ - WEG', 'Invoice number']
            )
            
            # Adiciona a coluna NF
            def get_nota_fiscal(row):
                try:
                    invoice_number = str(row['Invoice number']).strip()
                    
                    if invoice_number.startswith('QPE'):
                        # Busca no QPE_consolidado
                        if not qpe_data.empty and 'QPE_ID' in qpe_data.columns and 'NOTA_FISCAL' in qpe_data.columns:
                            matching_rows = qpe_data[qpe_data['QPE_ID'] == invoice_number]
                            if not matching_rows.empty:
                                matching_nota = matching_rows['NOTA_FISCAL'].iloc[0]
                                return str(matching_nota).strip()
                    elif invoice_number.startswith('SPB'):
                        # Busca no SPB_consolidado
                        if not spb_data.empty and 'SPB_ID' in spb_data.columns and 'Num_Nota' in spb_data.columns:
                            matching_rows = spb_data[spb_data['SPB_ID'] == invoice_number]
                            if not matching_rows.empty:
                                matching_nota = matching_rows['Num_Nota'].iloc[0]
                                return str(matching_nota).strip()
                    return ''
                except Exception as e:
                    print(f"Erro ao processar invoice number {invoice_number}: {str(e)}")
                    return ''
            
            grouped_data['NF'] = grouped_data.apply(get_nota_fiscal, axis=1)
            
            # Aplica o mapeamento para criar as novas colunas
            def get_material_and_type(row):
                try:
                    # Pega o código do serviço (antes do hífen, se houver)
                    service_code = str(row['Municipality Code']).strip().split(' - ')[0].strip()
                    
                    # Busca no mapeamento
                    if service_code in self.service_mapping:
                        return pd.Series([
                            self.service_mapping[service_code]['material'],
                            self.service_mapping[service_code]['type']
                        ])
                    return pd.Series(['', ''])
                except Exception as e:
                    print(f"Erro ao processar código de serviço {service_code}: {str(e)}")
                    return pd.Series(['', ''])
            
            # Aplica o mapeamento para criar as novas colunas
            grouped_data[['MATERIAL', 'Invoice_Type']] = grouped_data.apply(get_material_and_type, axis=1)
            
            # Reordena as colunas na ordem especificada
            grouped_data = grouped_data.reindex(columns=[
                'CNPJ - WEG',
                'Municipality Code',
                'MATERIAL',
                'Invoice_Type',
                'NF',
                'Site Name - WEG 2',
                'Total Geral'
            ])
            
            has_divergences = not cnpj_divergences.empty
            
            if has_divergences:
                message = f"Encontradas {len(cnpj_divergences)} divergências de CNPJ não autorizado."
            else:
                message = "Nenhuma divergência encontrada."
                
            message += f"\nForam geradas {len(grouped_data)} linhas após o agrupamento."
            
            return True, message, cnpj_divergences, grouped_data
            
        except Exception as e:
            return True, f"Erro ao verificar divergências: {str(e)}", pd.DataFrame(), pd.DataFrame()

    def generate_report(self) -> tuple[bool, str]:
        """
        Gera o relatório de divergências entre códigos municipais e R189.
        
        Returns:
            tuple contendo:
            - bool: True se o relatório foi gerado com sucesso, False caso contrário
            - str: Mensagem descritiva do resultado
        """
        try:
            # Busca os arquivos consolidados no SharePoint
            mun_code_file = self.sharepoint_auth.baixar_arquivo_sharepoint(
                'Municipality_Code_consolidado.xlsx',
                '/teams/BR-TI-TIN/AutomaoFinanas/CONSOLIDADO'
            )
            
            r189_file = self.sharepoint_auth.baixar_arquivo_sharepoint(
                'R189_consolidado.xlsx',
                '/teams/BR-TI-TIN/AutomaoFinanas/CONSOLIDADO'
            )
            
            if not mun_code_file or not r189_file:
                return False, "Não foi possível encontrar os arquivos consolidados no SharePoint."
            
            # Lê os arquivos em DataFrames
            mun_code_data = pd.read_excel(mun_code_file)
            r189_data = pd.read_excel(r189_file)
            
            # Verifica divergências e obtém dados agrupados
            has_data, message, divergences, grouped_data = self.check_divergences(mun_code_data, r189_data)
            
            if has_data:
                # Gera o arquivo de relatório
                report_file = BytesIO()
                with pd.ExcelWriter(report_file, engine='xlsxwriter') as writer:
                    # Aba de divergências (se houver)
                    if not divergences.empty:
                        divergences.to_excel(
                            writer, 
                            index=False, 
                            sheet_name='Divergencias_CNPJs'
                        )
                    
                    # Aba de dados agrupados
                    grouped_data.to_excel(
                        writer, 
                        index=False, 
                        sheet_name='Dados_Agrupados'
                    )
                    
                    # Ajusta o formato das colunas
                    workbook = writer.book
                    
                    # Formato para valores monetários
                    money_format = workbook.add_format({'num_format': '#,##0.00'})
                    
                    # Aplica formato nas abas
                    for sheet_name in writer.sheets:
                        worksheet = writer.sheets[sheet_name]
                        # Ajusta largura das colunas
                        for idx, col in enumerate(grouped_data.columns):
                            max_length = max(
                                grouped_data[col].astype(str).apply(len).max(),
                                len(col)
                            )
                            worksheet.set_column(idx, idx, max_length + 2)
                        
                        # Aplica formato monetário na coluna de total
                        for col in self.colunas_total:
                            if col in grouped_data.columns:
                                total_col = grouped_data.columns.get_loc(col)
                                worksheet.set_column(total_col, total_col, None, money_format)
                                break
                report_file.seek(0)
                
                # Define o nome do arquivo com timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                report_name = f'report_mun_code_r189_{timestamp}.xlsx'
                
                # Envia o relatório para o SharePoint
                self.sharepoint_auth.enviar_para_sharepoint(
                    report_file,
                    report_name,
                    '/teams/BR-TI-TIN/AutomaoFinanas/RELATÓRIOS/MUN_CODE'
                )
                
                message += f"\nRelatório gerado com sucesso: {report_name}"
            
            return True, message
            
        except Exception as e:
            return False, f"Erro ao gerar relatório: {str(e)}"