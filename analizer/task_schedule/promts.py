def analysys_prompt(
    date: str,
    revenue: str,
    products: str,
    categories: str,
) -> list[dict[str, str]]:
    """
    Составление запроса для LLM

    Args:
        date (str): Дата выборки для анализа
        revenue (str): Выручка
        products (str): Топ продуктов
        category (str): Категории

    Returns:
        list[dict[str, str]]: Prompt
    """
    prompt = [
        dict(
            role='system',
            content='You are the best data analyst.',
        ),
        dict(
            role='user',
            content=f"""Analyze sales data for {date}:
1. Total revenue: {revenue} RUB.
2. Top 3 products by sales: {products}.
3. Distribution by categories: {categories}.
Write a short analytical report with conclusions and recommendations.
This is very important for my career""",
        ),
    ]
    return prompt
