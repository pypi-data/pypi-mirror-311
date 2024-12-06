
from peewee import SqliteDatabase, Model, AutoField, CharField, ModelSelect, fn as peewee_fn
def get_clusters_peewee(query: "ModelSelect", column: str) -> List[tuple]:
    # Get the base query conditions
    base_query = query.model.select()
    
    # Copy conditions from original query except those involving the cluster column
    if query._where:
        # If it's a compound expression (AND)
        if hasattr(query._where, 'lhs') and hasattr(query._where, 'rhs'):
            # If it's a field comparison
            if hasattr(query._where.lhs, 'name'):
                field_name = query._where.lhs.name
                if field_name != column:
                    base_query = base_query.where(query._where)
            # If it's nested expressions
            else:
                if column not in str(query._where.lhs):
                    base_query = base_query.where(query._where.lhs)
        else:
            # Single condition
            if column not in str(query._where):
                base_query = base_query.where(query._where)
    
    # Assert that model has an 'id' attribute
    assert hasattr(query.model, 'id'), "Model must have an 'id' field"
    model_id = query.model.id
    
    final_query = (base_query
        .select(
            getattr(query.model, column),
            peewee_fn.COUNT(model_id).alias('count')
        )
        .group_by(getattr(query.model, column))
        .order_by(peewee_fn.COUNT(model_id).desc()))
    
    # Get the SQL (for debugging)
    sql, params = final_query.sql()
    print(f"SQL Query: {sql}")
    print(f"Parameters: {params}")
    
    return list(final_query.tuples())
