from pymatgen.core import Composition, Element

def is_max_phase(formula: str) -> bool:
    """
    Проверяет, соответствует ли химическая формула формальным критериям MAX-фазы.
    Возвращает словарь с результатами проверки.
    """
    comp = Composition(formula)
    elements = comp.elements  # это список объектов Element
    element_counts = comp.get_el_amt_dict()  # это dict[str, float]
    
    # 1. Проверка количества элементов (должно быть ровно 3 различных элемента)
    if len(elements) != 3:
        return False
    
    # 2. Определение возможных ролей элементов по стехиометрии
    # Ищем элемент с наименьшим количеством - это возможный A-элемент
    sorted_by_amount = sorted(element_counts.items(), key=lambda x: x[1])
    a_element_symbol, a_count = sorted_by_amount[0]
    
    # Оставшиеся два - M и X
    remaining = {k: v for k, v in element_counts.items() if k != a_element_symbol}
    
    # X - обычно C или N, количество меньше чем у M в типичных MAX-фазах
    # Ищем кандидата на X - обычно C или N с меньшим количеством
    m_candidates = {}
    x_candidate_symbol = None
    
    for el_symbol, cnt in remaining.items():
        if el_symbol in ['C', 'N']:
            x_candidate_symbol = el_symbol
            m_candidates = {k: v for k, v in remaining.items() if k != el_symbol}
            break
    
    # Если нет C или N, то X не определен
    if x_candidate_symbol is None:
        return False
    
    m_element_symbol = list(m_candidates.keys())[0] if m_candidates else None
    if m_element_symbol is None:
        return False
    
    m_count = remaining[m_element_symbol]
    x_count = remaining[x_candidate_symbol]
    
    # 3. Проверка стехиометрического соотношения M_{n+1}AX_n
    if x_count == 0:
        return False
    
    ratio = m_count / x_count
    tolerance = 0.1  # небольшая погрешность
    
    n_value = None
    if abs(ratio - 2.0) < tolerance:
        n_value = 1  # M2AX (211)
    elif abs(ratio - 1.5) < tolerance:
        n_value = 2  # M3AX2 (312)
    elif abs(ratio - 1.333) < tolerance:
        n_value = 3  # M4AX3 (413)
    elif abs(ratio - 1.25) < tolerance:
        n_value = 4  # M5AX4 (514)
    
    if n_value is None:
        return False
    
    # Ожидаемое количество A-элемента = 1
    if abs(a_count - 1.0) > tolerance:
        return False
    
    # 4. Проверка типов элементов
    # Получаем объекты Element для проверки блока и группы
    try:
        m_element = Element(m_element_symbol)
        a_element = Element(a_element_symbol)
        
        # M должен быть переходным металлом (d- или f-блок)
        m_block = m_element.block
        if m_block not in ['d', 'f']:
            return False
        
        # A должен быть из IIIA или IVA групп (13-16 группы по новой IUPAC)
        a_group = a_element.group
        # Группа может быть int или None для некоторых элементов
        if a_group is None or a_group not in [13, 14, 15, 16]:
            return False
        
        # X уже проверен как C или N
        if x_candidate_symbol not in ['C', 'N']:
            return False
            
    except Exception as e:
        return False
    
    # Все проверки пройдены
    return True