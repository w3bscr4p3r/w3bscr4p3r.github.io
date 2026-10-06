# WOLF Cyber Roadmap

**Da base técnica à decisão estratégica.**

Página interativa de planejamento de estudos em cibersegurança, organizada em **7 fases, 24 semanas e 192 horas**, com atividades práticas, critérios de conclusão e diário de evidências.

O projeto utiliza **HTML, CSS e JavaScript puro em um único arquivo**, sem instalação de dependências, backend ou banco de dados. A organização da jornada foi inspirada no [StudyPlan de w3bscr4p3r](https://github.com/w3bscr4p3r/w3bscr4p3r.github.io/tree/main/StudyPlan).

## Objetivo

Apoiar uma jornada de aprendizado que conecte fundamentos técnicos, proteção, automação, operações de segurança, resposta a incidentes, arquitetura e GRC.

A metodologia é **aprender → aplicar → comprovar**. O progresso representa entregas assinaladas pelo próprio estudante; não é uma avaliação automática de proficiência nem uma certificação.

## Funcionalidades

- Visão geral com sete cartões de fases e indicadores de progresso.
- Navegação por fases, com objetivos, pré-requisitos, conteúdos e laboratórios.
- **28 entregas verificáveis:** quatro por fase.
- Progresso global e por fase atualizado ao marcar ou desmarcar entregas.
- Botão para continuar na primeira fase ainda incompleta.
- Diário de evidências por fase, com até 12.000 caracteres.
- Salvamento automático do checklist e das anotações no navegador.
- Exportação e importação de backup JSON.
- Impressão de todas as fases, incluindo checklists, anotações e referências.
- Tema escuro, estilos responsivos e navegação horizontal no celular.
- Indicadores de foco, rótulos de formulário e respeito à preferência por movimento reduzido.

## Roadmap

| Fase | Tema | Semanas | Carga | Resultado esperado |
| --- | --- | --- | --- | --- |
| 01 | Fundamentos e laboratório | 1–3 | 24h | Laboratório isolado, diagrama e análise de tráfego |
| 02 | Identidade e proteção | 4–6 | 24h | Acessos validados, hardening e restauração de backup |
| 03 | Automação para segurança | 7–9 | 24h | Coleta, normalização e enriquecimento de eventos |
| 04 | SOC e engenharia de detecção | 10–13 | 32h | Cinco casos de detecção testados e procedimento de triagem |
| 05 | Investigação e resposta | 14–17 | 32h | Linha do tempo, relatório e dois playbooks |
| 06 | AppSec e arquitetura | 18–21 | 32h | Avaliação de aplicação, correções e retestes |
| 07 | GRC e projeto integrador | 22–24 | 24h | Registro de riscos, plano de 90 dias e apresentação executiva |
| **Total** | **7 fases** | **24 semanas** | **192h** | **Portfólio de evidências práticas** |

As semanas são uma sugestão de organização. Quem já possui experiência pode validar competências pelas entregas e dedicar mais tempo às lacunas identificadas.

### Rotina semanal sugerida

| Dia | Atividade | Tempo |
| --- | --- | --- |
| Segunda-feira | Conceitos e documentação | 1h30 |
| Terça-feira | Laboratório | 2h |
| Quarta-feira | Revisão | 1h |
| Quinta-feira | Testes práticos | 2h |
| Sexta-feira | Documentação | 1h30 |

## Arquivos

| Arquivo | Finalidade |
| --- | --- |
| `WOLF-Cyber-Roadmap.html` | Aplicação completa, incluindo CSS e JavaScript |
| `README.md` | Instruções de uso e manutenção |
| `wolf-roadmap-progresso.json` | Backup gerado pelo botão de exportação; não acompanha a aplicação |

Na hospedagem, o HTML pode ser renomeado para `index.html`.

## Como executar

### Abrir diretamente

1. Baixe `WOLF-Cyber-Roadmap.html`.
2. Abra o arquivo em um navegador moderno com JavaScript habilitado.
3. Clique em **Começar jornada** ou escolha uma fase.

A interface e o conteúdo incorporado funcionam sem internet ao abrir o arquivo local. As referências externas exigem conexão. O comportamento do armazenamento em endereços `file://` pode variar entre navegadores; mantenha backups ou utilize um servidor local.

### Servidor local opcional

Com Python 3 instalado, execute dentro da pasta que contém o HTML:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Abra:

```text
http://127.0.0.1:8000/WOLF-Cyber-Roadmap.html
```

Se renomeou o arquivo para `index.html`, acesse `http://127.0.0.1:8000/`.

Encerre o servidor com `Ctrl+C`. Python serve apenas os arquivos; não participa do funcionamento da aplicação.

## Publicação no GitHub Pages

Para adicionar o roadmap ao repositório `w3bscr4p3r.github.io`, a pasta sugerida é `CyberRoadmap/`:

1. Coloque o HTML como `CyberRoadmap/index.html` e este documento como `CyberRoadmap/README.md`.
2. Envie os arquivos para a branch utilizada na publicação.
3. Se o site já publica essa pasta por um workflow existente, mantenha a configuração e confirme o deploy.
4. Para uma nova configuração por branch, acesse **Settings → Pages → Build and deployment**, selecione **Deploy from a branch**, escolha a branch e a raiz `/(root)`, e salve.

Com a raiz do repositório publicada, o endereço esperado será:

```text
https://w3bscr4p3r.github.io/CyberRoadmap/
```

Esse é um endereço sugerido para depois da publicação; este README não indica que o deploy já foi realizado. Preserve a pasta `StudyPlan/` caso queira manter o projeto escolar original.

Referência: [configuração da origem de publicação — GitHub Docs](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Como usar

1. Leia os objetivos e pré-requisitos da fase.
2. Estude os tópicos e consulte as referências.
3. Execute o laboratório em ambiente próprio ou autorizado.
4. Documente resultados e limitações no **Meu diário de evidências**.
5. Marque somente as entregas que conseguiu demonstrar.
6. Exporte seu progresso periodicamente.

O diário registra texto e referências a evidências. Ele não faz upload nem armazena os arquivos do laboratório.

### Progresso

Cada entrega possui o mesmo peso no indicador global:

```text
Progresso (%) = arredondar(entregas concluídas / 28 × 100)
```

Cada fase avança 25 pontos percentuais por entrega. O indicador não mede horas efetivamente estudadas. As fases permanecem acessíveis independentemente do checklist.

### Backup e restauração

- **Exportar progresso:** baixa `wolf-roadmap-progresso.json`.
- **Importar:** permite selecionar um backup e confirmar a substituição dos dados atuais.
- A importação substitui o progresso e as anotações; não faz mesclagem.
- Arquivos acima de 200.000 bytes ou com estrutura incompatível são rejeitados.

Exemplo simplificado de backup:

```json
{
  "version": 1,
  "checks": {
    "0-0": true,
    "0-1": false
  },
  "notes": {
    "0": "Laboratório criado; diagrama e captura de rede registrados."
  },
  "exportedAt": "2026-10-06T20:00:00.000Z"
}
```

Os índices começam em zero: `0-0` identifica a primeira entrega da primeira fase. `exportedAt` é acrescentado à exportação como informação; a restauração utiliza `version`, `checks` e `notes`.

### Impressão e PDF

Clique em **Imprimir / PDF** e use a opção de salvar como PDF oferecida pelo navegador. A impressão reúne todas as fases, mesmo quando apenas uma está aberta. O PDF é um relatório; use o JSON para restaurar o progresso.

## Armazenamento e privacidade

O estado é armazenado em `localStorage`, na chave:

```text
wolf-cyber-roadmap-v1
```

A aplicação não implementa envio de anotações a um servidor, autenticação, analytics ou sincronização. Links externos levam a serviços com políticas próprias.

- Os dados ficam vinculados ao navegador, perfil e origem utilizados.
- Alterar domínio, protocolo ou porta pode apresentar um armazenamento diferente.
- Limpar os dados do site pode apagar o progresso; navegação privada pode descartá-lo ao encerrar a sessão.
- Instâncias com a mesma chave na mesma origem compartilham o estado, mesmo em pastas distintas.
- As anotações e o backup JSON não são criptografados pela aplicação. Evite senhas, tokens e evidências sensíveis.
- Se surgir um aviso de falha no salvamento, exporte os dados antes de fechar a página.

## Personalização

Todo o código está no HTML:

| Local | O que alterar |
| --- | --- |
| `<style>` e variáveis em `:root` | Cores, espaçamentos, tipografia e layout |
| Cabeçalho, hero e rodapé | Nome, identidade visual e textos de apresentação |
| Array JavaScript `phases` | Conteúdo, laboratório, entregas e referências de cada fase |
| Função `weekly()` | Rotina semanal apresentada |
| Constante `KEY` | Identificador do armazenamento local |
| Função `printContent()` | Conteúdo do relatório impresso |

Cada fase contém `title`, `short`, `weeks`, `hours`, `summary`, `goal`, `pre`, `topics`, `lab`, `checks` e `refs`.

**Ao alterar a quantidade de fases ou entregas**, revise também os totais fixos da interface e do cálculo: sete fases, quatro entregas por fase, 28 entregas, 24 semanas e 192 horas. Esses valores não são todos derivados automaticamente do array.

O progresso utiliza índices posicionais. Reordenar fases ou entregas pode associar registros antigos a conteúdos diferentes. Para mudanças estruturais, planeje uma migração ou use uma nova chave de armazenamento e versão de backup compatível.

## Limitações da versão 1.0

- Não há contas de usuário, painel de instrutor ou sincronização entre dispositivos.
- Não há anexos, correção automática de exercícios ou emissão de certificados.
- Não há cronômetro, calendário editável, lembretes ou integração com plataformas de cursos.
- Não há service worker; o site hospedado não garante disponibilidade offline após fechar o navegador.
- O progresso é autodeclarado; a aplicação não valida as evidências.
- As referências externas podem mudar de endereço ou disponibilidade.

## Verificação realizada

A implementação passou por verificação de sintaxe JavaScript e testes em DOM simulado para navegação, checklist, armazenamento, escape das anotações, exportação, importação e geração do conteúdo de impressão. Foram conferidos os totais de sete fases e 192 horas.

A validação visual em navegador real não foi concluída no ambiente de criação. Recomenda-se conferir desktop, celular e impressão no navegador utilizado para publicação.

## Solução de problemas

| Situação | Verificação ou solução |
| --- | --- |
| Conteúdo das fases não aparece | Habilite JavaScript e abra o HTML em um navegador, não em um visualizador de texto |
| Progresso não permanece | Verifique o aviso de armazenamento, use o mesmo endereço e perfil ou restaure o backup |
| Backup não importa | Utilize um JSON exportado pela aplicação, com versão 1 e dentro do limite de tamanho |
| Progresso mudou após editar o roadmap | Confira se a ordem das fases ou entregas foi alterada |
| GitHub Pages retorna 404 | Confira pasta, nome `index.html`, origem de publicação e resultado do deploy |
| PDF não contém as fases | Use o botão da aplicação e confirme que JavaScript está ativo |

## Créditos e licença

Projeto apresentado sob a identidade **WOLF Cyber Security**, para a jornada de aprendizado de Daniel Alves.

A organização por fases foi inspirada no [StudyPlan de w3bscr4p3r](https://github.com/w3bscr4p3r/w3bscr4p3r.github.io/tree/main/StudyPlan). Os materiais externos pertencem aos seus respectivos autores e organizações; sua inclusão não implica parceria ou endosso.

**Licença de distribuição ainda não definida neste pacote.** Caso o projeto seja disponibilizado para reutilização, inclua um arquivo `LICENSE` com os termos escolhidos pelo titular. Este README não atribui uma licença aos materiais de terceiros.
