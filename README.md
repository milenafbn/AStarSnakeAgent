# Intelligent Snake Solver

Este projeto é parte de uma atividade acadêmica para a disciplina de Inteligência Artificial. Ele implementa um agente inteligente baseado em objetivos capaz de resolver problemas de forma autônoma utilizando o algoritmo A*. O ambiente de teste escolhido é uma versão simplificada do jogo Snake.

## Descrição

O objetivo do agente é maximizar sua pontuação no jogo Snake. Para isso, ele:
- Percebe o ambiente, incluindo a posição da comida e os limites do tabuleiro.
- Determina ações válidas que evitam colisões com o corpo da cobra ou com as paredes.
- Planeja um caminho até a comida utilizando o algoritmo A*, otimizando a trajetória para alcançar o objetivo.

O projeto inclui:
- Um ambiente visual em Pygame.
- A implementação de um agente inteligente com habilidades de planejamento e decisão.

## Tecnologias

- **Python 3.10+**
- **Pygame**: Para visualização e interação.
- **Algoritmo A***: Para planejamento de caminhos.

## Como Executar

### Pré-requisitos
- Python instalado (3.10 ou superior).
- Pygame instalado. Para instalar, execute:
  ```bash
  pip install pygame

1. Clone este repositório:
   ```bash
   git clone https://github.com/milenafbn/AStarSnakeAgent.git
2. Navegue até o diretório do projeto:
   ```bash
   cd AStarSnakeAgent
3. Run the script:
   ```bash
   python main.py

### Controles

O agente é totalmente autônomo, e não requer interação do usuário. A execução do jogo termina quando o agente não encontra mais movimentos válidos.

## Estrutura
- SnakeAgent: Implementa o agente inteligente, incluindo o algoritmo A* para planejamento de trajetórias.
- GameEnvironment: Gerencia a visualização do jogo e a interação com o agente.
- Algoritmo A*: Implementado dentro da classe SnakeAgent. Otimiza a busca por trajetórias no ambiente do jogo.

## Desempenho
Durante a execução, as seguintes métricas de desempenho são atualizadas e exibidas:
- Pontuação: Incrementada ao comer comida, reduzida ao se mover sem comer.
- Movimentos realizados: Contabiliza todos os passos feitos pelo agente.
- Comida coletada: Mostra o total de itens de comida consumidos.