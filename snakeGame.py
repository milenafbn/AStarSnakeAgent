import pygame
import random
import heapq
import sys
from collections import deque

class SnakeAgent:
    
    def __init__(self, grid_size):
        self.position = (5, 5)  # Posição inicial
        self.body = [(5, 5)]    # Corpo inicial
        self.grid_size = grid_size # Tamanho do tabuleiro
        self.score = 0          # Pontuação
        self.moves = 0          # Quantidade de movimentos
        self.food_collected = 0  # Comida coletada
        self.possible_actions = [
            (0, 1),   # direita
            (0, -1),  # esquerda
            (1, 0),   # baixo
            (-1, 0)   # cima
        ]
    
    def sense_environment(self, food_position): # sensor
        return {
            'current_position': self.position,
            'body': self.body,
            'food_position': food_position,
            'grid_size': self.grid_size
        }
    
    def get_valid_actions(self, environment): # ações válidas (não colide)
        valid_actions = []
        for action in self.possible_actions:
            new_pos = (
                self.position[0] + action[0],
                self.position[1] + action[1]
            )
            if self.is_valid_move(new_pos, environment):
                valid_actions.append(action)
        return valid_actions
    
    def is_valid_move(self, position, environment): # verifica se o movimento é válido
        x, y = position
        return (0 <= x < self.grid_size and 
                0 <= y < self.grid_size and 
                position not in self.body[:-1])
    
    def get_action_cost(self, current_state, next_state): # custo da ação
        food_pos = current_state['food_position']
        current_distance = self.manhattan_distance(current_state['current_position'], food_pos)
        next_distance = self.manhattan_distance(next_state, food_pos)
        
        # penalidade para movimentos que se afastam da comida
        if next_distance > current_distance:
            return 1.5
        return 1.0
    
    def manhattan_distance(self, pos1, pos2): # distância de Manhattan
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def a_star(self, environment): # algoritmo A*
        start = self.position
        goal = environment['food_position']
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return path
            
            for action in self.possible_actions:
                neighbor = (current[0] + action[0], current[1] + action[1])
                if not self.is_valid_move(neighbor, environment):
                    continue
                    
                tentative_g_score = g_score[current] + self.get_action_cost(environment, neighbor)
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None
    
    def reconstruct_path(self, came_from, current): # reconstrói o caminho
        path = [current]
        while current in came_from and came_from[current] is not None:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def act(self, environment): # determina e executa a próxima ação do agente
        path = self.a_star(environment)
        
        if path and len(path) > 1:
            next_pos = path[1]
            direction = (
                next_pos[0] - self.position[0],
                next_pos[1] - self.position[1]
            )
        else:
            # Movimento de fallback se não houver caminho direto
            valid_actions = self.get_valid_actions(environment)
            if valid_actions:
                direction = valid_actions[0]
            else:
                return None  # Sem movimentos válidos - fim de jogo
        
        # Atualiza estado do agente
        self.moves += 1
        new_position = (
            self.position[0] + direction[0],
            self.position[1] + direction[1]
        )
        self.position = new_position
        self.body.insert(0, new_position)
        
        return direction
    
    def update_performance(self, food_eaten): # atualiza o desempenho
        if food_eaten:
            self.score += 100
            self.food_collected += 1
        else:
            self.body.pop()
            self.score -= 1  # penalidade por movimento sem comer

class GameEnviroment:
    def __init__(self):
        pygame.init()
        self.WIDTH = 400
        self.HEIGHT = 400
        self.GRID_SIZE = 20
        self.ROWS = self.HEIGHT // self.GRID_SIZE
        self.COLS = self.WIDTH // self.GRID_SIZE
        self.font = pygame.font.SysFont("Arial", 20)

        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake - Agente Inteligente")
        
        # Cores
        self.GREEN_0 = (104, 147, 79) # #68934f
        self.GREEN_1 = (82, 119, 59) #52773b
        self.GREEN_2 = (47, 63, 41) #2f3f29
        self.RED = (147, 79, 79) #934f4f
        self.WHITE = (255, 255, 255)
        
        # Inicializa o agente e o ambiente
        self.agent = SnakeAgent(self.ROWS)
        self.food = self.generate_food()
        
    def generate_food(self): # gera a comida
        while True:
            food = (
                random.randint(0, self.ROWS - 1),
                random.randint(0, self.COLS - 1)
            )
            if food not in self.agent.body:
                return food
    
    def draw(self):
        self.screen.fill(self.GREEN_0)
        self.draw_grid()
        self.draw_snake()
        self.draw_food()
        pygame.display.flip()
    
    def draw_grid(self): # desenha a grade
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GREEN_1, (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GREEN_1, (0, y), (self.WIDTH, y))
    
    def draw_snake(self): # desenha a cobra
        for segment in self.agent.body:
            pygame.draw.rect(self.screen, self.GREEN_2,
                           (segment[1] * self.GRID_SIZE,
                            segment[0] * self.GRID_SIZE,
                            self.GRID_SIZE, self.GRID_SIZE))
    
    def draw_food(self): # desenha a comida
        pygame.draw.rect(self.screen, self.RED,
                        (self.food[1] * self.GRID_SIZE,
                         self.food[0] * self.GRID_SIZE,
                         self.GRID_SIZE, self.GRID_SIZE))
    
    def draw_performance(self):
        score_text = f"Score: {self.agent.score}"
        moves_text = f"Moves: {self.agent.moves}"
        food_text = f"Food: {self.agent.food_collected}"

        score_surface = self.font.render(score_text, True, self.WHITE)
        moves_surface = self.font.render(moves_text, True, self.WHITE)
        food_surface = self.font.render(food_text, True, self.WHITE)

        self.screen.blit(score_surface, (10, 10)) 
        self.screen.blit(moves_surface, (10, 30))
        self.screen.blit(food_surface, (10, 50))
    
    def run(self): # executa o jogo
        clock = pygame.time.Clock()
        running = True
        
        while running:
            clock.tick(10) 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # o agente percebe o ambiente e age
            environment = self.agent.sense_environment(self.food)
            direction = self.agent.act(environment)
            
            if direction is None:
                print("Game Over!")
                print(f"Score: {self.agent.score}")
                print(f"Food collected: {self.agent.food_collected}")
                print(f"Moves made: {self.agent.moves}")
                sys.stdout.flush() 
                running = False
                break
            
            # Verifica se comeu a comida
            food_eaten = self.agent.position == self.food
            if food_eaten:
                self.food = self.generate_food()
            
            # Atualiza o desempenho do agente
            self.agent.update_performance(food_eaten)
            
            # Atualiza a visualização
            self.draw()
            self.draw_performance()
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = GameEnviroment()
    game.run()