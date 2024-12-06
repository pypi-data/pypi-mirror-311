from sqlalchemy import inspect
from typing import Any

def where_clause_to_str(query: Any) -> str:
    """
    Convert SQLAlchemy query where clauses to readable SQL/English text.
    
    Args:
        query: SQLAlchemy query object
    
    Returns:
        str: Human-readable string representation of where clauses
    """
    # Extract where clauses from query
    whereclause = query._where_criteria
    if not whereclause:
        return "No where clauses"
        
    # Convert tuple to list
    whereclause = list(whereclause)
    
    def _process_binary_expression(expr):
        left = expr.left.name if hasattr(expr.left, 'name') else str(expr.left)
        right = expr.right.value if hasattr(expr.right, 'value') else str(expr.right)
        operator = expr.operator.__name__
        
        # Map common operators to readable text
        operator_map = {
            'eq': '=',
            'ne': '!=',
            'gt': '>',
            'lt': '<',
            'ge': '>=',
            'le': '<=',
            'like': 'LIKE',
            'ilike': 'ILIKE',
            'in_': 'IN',
        }
        
        op_str = operator_map.get(operator, operator)
        return f"{left} {op_str} {right}"
    
    def _process_clause(clause):
        if isinstance(clause, tuple):
            # Handle tuple of clauses
            return ' AND '.join(_process_clause(c) for c in clause)
        elif hasattr(clause, 'operator'):
            if hasattr(clause, 'clauses'):
                # Handle AND/OR conditions
                subclauses = [_process_clause(c) for c in clause.clauses]
                operator = ' AND ' if clause.operator.__name__ == 'and_' else ' OR '
                return f"({operator.join(subclauses)})"
            return _process_binary_expression(clause)
        return str(clause)
    
    # Process all clauses and join with AND
    processed_clauses = [_process_clause(clause) for clause in whereclause]
    return ' AND '.join(processed_clauses) if len(processed_clauses) > 1 else processed_clauses[0]

if __name__ == "__main__":
    # Create a test database and model
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.orm import declarative_base, Session

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        age = Column(Integer)

    # Create in-memory database
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # Create a test query
    with Session(engine) as session:
        # Test simple condition
        query1 = session.query(User).filter(User.age >= 18)
        print("Query 1:", where_clause_to_str(query1))

        # Test multiple conditions
        query2 = session.query(User).filter(
            User.age >= 18,
            User.name.like('%John%')
        )
        print("Query 2:", where_clause_to_str(query2))

        # Test OR condition
        from sqlalchemy import or_
        query3 = session.query(User).filter(
            or_(User.age < 18, User.name == 'Admin')
        )
        print("Query 3:", where_clause_to_str(query3))
