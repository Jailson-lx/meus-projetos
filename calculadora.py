import re
from math import sqrt

def is_perfect_square(n):
    # Verifica se n é um quadrado perfeito
    root = int(sqrt(n))
    return root * root == n

def simplify_root(n):
    # Simplifica raiz se for quadrada perfeita (ex.: r9 -> 3)
    if is_perfect_square(n):
        return int(sqrt(n)), 1  # Retorna coeficiente e raiz simplificada
    return 1, n  # Raiz não simplificada (ex.: r3 -> 1, 3)

def parse_number(s):
    # Remove espaços e tenta interpretar a entrada
    s = s.strip()
    
    # Substitui vírgula por ponto para números decimais (ex.: "9,2" -> "9.2")
    if ',' in s:
        s = s.replace(',', '.', 1)  # Substitui apenas a primeira vírgula
    
    # Regex para capturar números com raízes (ex.: "3r2" -> 3 * r2)
    match = re.match(r'^(\d+)?r(\d+)$', s)
    if match:
        coef = int(match.group(1)) if match.group(1) else 1  # Coeficiente (ex.: 3 em "3r2")
        root = int(match.group(2))  # Raiz (ex.: 2 em "r2")
        root_coef, simplified_root = simplify_root(root)
        return coef * root_coef, simplified_root  # Retorna (coeficiente total, raiz)
    
    try:
        # Tenta converter para float (aceita "5", "9.2", "9,2" após substituição)
        return float(s), 1  # Número simples (ex.: "9.2" -> 9.2, 1)
    except ValueError:
        raise ValueError(f"Formato inválido: {s}")

def format_result(coef, root):
    # Formata o resultado (ex.: (3, 3) -> "3r3", (5, 1) -> "5")
    if root == 1:
        # Se coef for inteiro, exibe como inteiro; senão, usa até 4 casas decimais
        if coef.is_integer():
            return str(int(coef))
        return f"{coef:.4f}".rstrip('0').rstrip('.')
    if coef == 1:
        return f"r{root}"
    # Se coef for inteiro, exibe como inteiro; senão, usa até 4 casas decimais
    if coef.is_integer():
        return f"{int(coef)}r{root}"
    return f"{coef:.4f}".rstrip('0').rstrip('.') + f"r{root}"

def calculate_surface_area(a_coef, a_root, b_coef, b_root, c_coef, c_root):
    # Calcula área: 2 * (ab + bc + ac)
    ab_coef = a_coef * b_coef
    ab_root = a_root * b_root
    bc_coef = b_coef * c_coef
    bc_root = b_root * c_root
    ac_coef = a_coef * c_coef
    ac_root = a_root * c_root

    # Agrupa termos por raiz
    terms = {}
    for coef, root in [(ab_coef, ab_root), (bc_coef, bc_root), (ac_coef, ac_root)]:
        if root in terms:
            terms[root] += coef
        else:
            terms[root] = coef

    # Calcula a área total: 2 * soma dos termos
    result = []
    for root, coef in sorted(terms.items(), key=lambda x: x[0]):  # Ordena por raiz
        if abs(coef) > 1e-10:  # Ignora termos com coeficiente muito pequeno
            term = 2 * coef  # Multiplica por 2 (fórmula)
            if abs(term) > 1e-10:
                result.append(format_result(term, root))

    # Formata o resultado final
    if not result:
        return "0"
    return " + ".join(result)

def main():
    print("Digite as dimensões a, b, c (ex.: 5, 3r2 para 3√2, r9 para 3, 9,2 para 9.2):")
    try:
        # Lê as entradas com tratamento de EOFError e entradas vazias
        a_input = input("a: ").strip() or "2"  # Valor padrão: 2
        if not a_input:
            raise ValueError("Entrada para 'a' não fornecida")
        b_input = input("b: ").strip() or "r2"  # Valor padrão: r2
        if not b_input:
            raise ValueError("Entrada para 'b' não fornecida")
        c_input = input("c: ").strip() or "3r9"  # Valor padrão: 3r9
        if not c_input:
            raise ValueError("Entrada para 'c' não fornecida")

        # Converte as entradas
        a_coef, a_root = parse_number(a_input)
        b_coef, b_root = parse_number(b_input)
        c_coef, c_root = parse_number(c_input)

        # Calcula a área
        area = calculate_surface_area(a_coef, a_root, b_coef, b_root, c_coef, c_root)

        # Exibe o resultado
        print(f"Área total = {area}")
    except EOFError:
        # Se ocorrer EOFError, usa valores padrão
        print("Erro: Entrada interrompida (EOF). Usando valores padrão (a=2, b=r2, c=3r9).")
        a_coef, a_root = parse_number("2")
        b_coef, b_root = parse_number("r2")
        c_coef, c_root = parse_number("3r9")
        area = calculate_surface_area(a_coef, a_root, b_coef, b_root, c_coef, c_root)
        print(f"Área total = {area}")
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
