import getpass
import warnings
import os
import uuid
import datetime

import pyautogui
import pytesseract
from pywinauto.application import Application
from PIL import Image, ImageEnhance
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
    send_file,
    get_historico_by_processo_identificador,
)

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    is_window_open,
    is_window_open_by_class,
    kill_process,
    login_emsys_fiscal,
    set_variable,
    type_text_into_field,
    worker_sleep,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def sped_fiscal(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que realiza as atividades de Sped no ERP EMSys(Linx) Fiscal.

    """
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        # Seta config entrada na var sped_processar para melhor entendimento
        sped_processar = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_process("EMSysFiscal")

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSysFiscal.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        await worker_sleep(4)
        max_attempts = 15
        i = 0
        while i < max_attempts:
            console.print("Aguardando o EMSys Fiscal...\n")
            login_module = await is_window_open_by_class("TFrmLoginModulo", "TFrmLoginModulo")
            if login_module["IsOpened"] == True:
                break
            else:
                i = i+1
        
        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir o EMSys Fiscal, tela de login não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        
        return_login = await login_emsys_fiscal(config.conConfiguracao, app, task)
        if return_login.sucesso == True:
            type_text_into_field(
                "Sped Fiscal", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Sped Fiscal' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(6)
        console.print("Verificando se a janela para gerar Sped foi aberta com sucesso...\n")
        max_attempts = 15
        i = 0
        while i < max_attempts:
            gerar_sped = await is_window_open_by_class("TFrmGerarSpeed", "TFrmGerarSpeed")
            if gerar_sped["IsOpened"] == True:
                console.print("janela para gerar Sped foi aberta com sucesso...\n")
                break
            else:
                await worker_sleep(1)
                i = i+1
        
        if i >= max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro ao abrir a janela para gerar o Sped Fiscal, tela não encontrada",
                status=RpaHistoricoStatusEnum.Falha,
            )
        
        filial_cod = sped_processar.get("empresa")
        periodo_dt = sped_processar.get("periodo")
        
        #DIRETORIO TEMPORARIO ANTES DE SER MOVIDO PARA O GOOGLE DRIVE
        username = getpass.getuser()
        short_uuid = str(uuid.uuid4()).replace('-', '')[:6]
        temp_path_to_txt = f"C:\\Users\\{username}\\Downloads\\{short_uuid}_{filial_cod}.txt"
        console.print(f"Diretório temporario: {temp_path_to_txt}...\n")
        
        console.print("Navegando pela Janela de Gerar Sped Fiscal...\n")
        try:
            app = Application().connect(class_name="TFrmGerarSpeed")
            main_window = app["TFrmGerarSpeed"]

            main_window.set_focus()
            console.print("Preenchendo as informações necessarias para gerar o sped fiscal... \n")
            panel_TPage = main_window.child_window(class_name="TcxPageControl")
            panel_TTabSheet = panel_TPage.child_window(class_name="TcxTabSheet")
            panel_TTabSheet.wait("visible")

            console.print("Inserindo o diretório temporario para geração do sped...\n")
            filename = panel_TTabSheet.child_window(class_name="TFilenameEdit")
            filename.set_edit_text(temp_path_to_txt)
            await worker_sleep(2)

            console.print("Inserindo o período para geração do sped...\n")
            periodo = panel_TTabSheet.child_window(class_name="TDBIEditDate", found_index=2)
            periodo.set_edit_text(periodo_dt)
            await worker_sleep(1)

            console.print("Selecionando a opção Gerar E115...\n")
            checkbox_gerar_e115 = main_window.child_window(class_name="TDBICheckBox", found_index=8)
            if not checkbox_gerar_e115.get_toggle_state() == 1:
                checkbox_gerar_e115.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(1)
            

            console.print("Selecionando a opção Gerar valores zerados para notas de cfop 5929 e 6929...\n")
            checkbox_gerar_cfop= main_window.child_window(class_name="TCheckBox", found_index=3)
            if not checkbox_gerar_cfop.get_toggle_state() == 1:
                checkbox_gerar_cfop.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(1)

            console.print("Selecionando a opção Gerar valores zerados para IPI...\n")
            checkbox_valores_ipi = main_window.child_window(class_name="TCheckBox", found_index=1)
            if not checkbox_valores_ipi.get_toggle_state() == 1:
                checkbox_valores_ipi.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(1)
            

            console.print("Gerar valores zerados para Base ST e Icms ST...\n")
            checkbox_gerar_base_ct_icms_st = main_window.child_window(class_name="TCheckBox", found_index=2)
            if not checkbox_gerar_base_ct_icms_st.get_toggle_state() == 1:
                checkbox_gerar_base_ct_icms_st.click()
                console.print("Selecionado com sucesso... \n")
                await worker_sleep(1)
            
            console.print("Todos os campos selecionados com sucesso, seguindo para geração do Sped Fiscal...\n")
        except Exception as e:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao interagir com a tela de gerar sped fiscal, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )
            

        await worker_sleep(2)
        pesquisar_full_path = "assets\\entrada_notas\\button_gerar_sped_fiscal.png"
        try:
            button_location = pyautogui.locateCenterOnScreen(pesquisar_full_path, confidence=0.6)
            if button_location:
                pyautogui.click(button_location)
                console.print("Botão 'Gerar Sped' clicado com sucesso!")
        except pyautogui.ImageNotFoundException:
            window_rect = main_window.rectangle()
            console.print(f"Area que sera utulizada para o recorte {window_rect}...\n")
            try:
                button_location = pyautogui.locateCenterOnScreen(pesquisar_full_path, region=(window_rect.left, window_rect.top, window_rect.width(), window_rect.height()))
                if button_location:
                    button_location = (button_location.x + window_rect.left, button_location.y + window_rect.top)
                    console.print(f"Botão encontrado nas coordenadas: {button_location}")
                    pyautogui.click(button_location)
            except pyautogui.ImageNotFoundException:
                console.print("Erro - Botão de gerar o sped na tela de Gerar Sped Fiscal")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno="Erro - Botão de gerar o sped na tela de Gerar Sped Fiscal",
                    status=RpaHistoricoStatusEnum.Falha,
                )
        except Exception as e:
            console.print(
                f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de gerar sped na tela Gerar Sped Fiscal,Error: {e}...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel seguir pois não foi fois possivel interagir com o botão de gerar sped na tela Gerar Sped Fiscal,Error: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )


        max_attempts = 75
        i = 0
        while i < max_attempts:
            aviso_gerando_sped_full_path = "assets\\entrada_notas\\gerando_sped_fiscal.png.png"
            sped_gerado_element = False
            sped_gerado_ui = False
            try:
                aviso_gerando_sped_full_path = pyautogui.locateCenterOnScreen(aviso_gerando_sped_full_path, confidence=0.6)
                if aviso_gerando_sped_full_path:
                    console.print(f"Gerando o arquivo Sped Fiscal...\n")
                else:
                    sped_gerado_ui = True
            except:
                console.print(f"Tela de gerando sped não encontrada, verificando via elemento para dupla confirmação...\n")
                sped_gerado_ui = True
            
            aguardar_sped = await is_window_open_by_class("TFrmAguarde", "TFrmAguarde")
            if aguardar_sped["IsOpened"] == False:
                sped_gerado_element = True

            if sped_gerado_element and sped_gerado_ui:
                console.print("Confirmação dupla: Nenhum indicador de SPED em progresso encontrado. Saindo do loop...\n")
                break
            else:
                i += 1
                console.print(f"Gerando o arquivo Sped Fiscal, Tentativa {i}/{max_attempts}: Aguarde mais 120 segundos...\n")
                await worker_sleep(120)


        # Verificando se possui pop-up de Aviso 
        await worker_sleep(6)
        warning_pop_up = await is_window_open("Aviso")
        if warning_pop_up["IsOpened"] == True:
            app = Application().connect(title="Aviso")
            main_window = app["Aviso"]
            main_window.set_focus()

            console.print(f"Obtendo texto do Aviso...\n")
            console.print(f"Tirando print da janela do warning para realização do OCR...\n")

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = f"C:\\Users\\{username}\\Downloads\\aviso_popup_{short_uuid}_{filial_cod}.png"
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(
                f"Texto Full capturado {captured_text}...\n"
            )
            os.remove(path_to_png)
            if 'movimento não permitido' in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Filial: {filial_cod} está com o livro fechado ou encerrado, verificar com o setor fiscal",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            elif 'não foi possiv' in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Filial: {filial_cod} Não foi possível gerar o SPED, devido a mensagem: {captured_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            elif 'informe o tipo de' in captured_text.lower():
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Mensagem do Aviso, Informe o tipo cobraça ",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            else:
                return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Aviso não mapeado para seguimento do robo, mensagem: {captured_text}",
                status=RpaHistoricoStatusEnum.Falha,
                )
        else:
            console.print(f"POP-up aviso não encontrado...\n")

        
        # Verifica se a info 'Arquivo do SPED gerado com sucesso' está na tela
        await worker_sleep(6)
        try:
            max_attempts = 60
            i = 0

            while i < max_attempts:
                information_pop_up = await is_window_open("Informação")
                if information_pop_up["IsOpened"] == True:
                    break
                else:
                    console.print(f"Aguardando confirmação de nota incluida...\n")
                    await worker_sleep(5)
                    i += 1

            app = Application().connect(class_name="TMsgBox")
            main_window = app["Informação"]

            main_window.set_focus()

            console.print(f"Obtendo texto do Informação...\n")
            console.print(f"Tirando print da janela do Information para realização do OCR...\n")

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = f"C:\\Users\\{username}\\Downloads\\information_popup_{short_uuid}_{filial_cod}.png"
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(
                f"Texto Full capturado {captured_text}...\n"
            )
            os.remove(path_to_png)
            if 'arquivo do sped ger' in captured_text.lower():
                console.print("\nArquivo do SPED gerado com sucesso...", style="bold green")
                await worker_sleep(6)

                console.log("Realizando o envio para o Backoffice...\n")
                file_bytes = ""
                with open(temp_path_to_txt, 'rb') as file:
                    file_bytes = file.read()
                

                get_historico = get_historico_by_processo_identificador(filial_cod, task.nomProcesso)
                if get_historico["sucesso"] == True:
                    data = get_historico["retorno"]
                    id_historico = data[0]['uuidHistorico']
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    desArquivo = f"ArquivoSped_{filial_cod}_{timestamp}.txt"
                    try:
                        send_file(id_historico, desArquivo, "text", file_bytes, file_extension="txt")
                        result = "Arquivo do SPED gerado com sucesso e arquivo salvo no Backoffice !"
                        os.remove(temp_path_to_txt)
                        return RpaRetornoProcessoDTO(
                            sucesso=True,
                            retorno=result,
                            status=RpaHistoricoStatusEnum.Sucesso,
                        )
                    except Exception as e:
                        result = f"Arquivo do SPED gerado com sucesso, porém gerou erro ao realizar o envio para o backoffice {e} - Arquivo ainda salvo na dispositivo utilizado no diretório {temp_path_to_txt} !"
                        console.print(result, style="bold red")
                        
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=result,
                            status=RpaHistoricoStatusEnum.Falha,
                        )
                else:
                    result = f"Arquivo do SPED gerado com sucesso, porém não foi possivel obter o id do historico para envio do arquivo, retorno {get_historico["retorno"]}  - Arquivo ainda salvo na dispositivo utilizado no diretório {temp_path_to_txt}"
                    console.print(result, style="bold red")
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=result,
                        status=RpaHistoricoStatusEnum.Falha,
                    )
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Pop_up Informação não mapeado para andamento do robô, mensagem {captured_text}",
                    status=RpaHistoricoStatusEnum.Falha,
                )
        except Exception as e:
            console.print(f"Erro ao conectar à janela Informação: {e}\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro em obter o retorno, Arquivo do SPED gerado com sucesso, erro {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

    except Exception as ex:
        observacao = f"Erro ao gerar o Arquivo do SPED: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}
