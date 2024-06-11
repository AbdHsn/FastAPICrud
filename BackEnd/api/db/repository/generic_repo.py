from typing import Type, Generic, TypeVar, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, update, delete, and_, or_
from schemas.all_by_where_schema import GetAllByWhereGLB
from schemas.count_by_where_schema import CountByWhereGLB

T = TypeVar('T')  # Type variable for SQLAlchemy model class

class GenericRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_field(self, **kwargs):
        try:
            async with self.session.begin():
                query = select(self.model).filter_by(**kwargs)
                result = await self.session.execute(query)
                return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            return None
    
    async def get_by_field(self, and_conditions=None, or_conditions=None):
        try:
            async with self.session.begin():
                query = select(self.model)
                
                if and_conditions:
                    query = query.filter(and_(*[getattr(self.model, k) == v for k, v in and_conditions.items()]))
                
                if or_conditions:
                    query = query.filter(or_(*[getattr(self.model, k) == v for k, v in or_conditions.items()]))

                result = await self.session.execute(query)
                return result.scalars().first()
        except SQLAlchemyError as e:
            await self.session.rollback()
            return None
    
    async def insert(self, entity: T):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, identifier_field: str, identifier_value: Any, **updated_fields) -> Optional[T]:
        async with self.session as session:
            stmt = (
                update(self.model)
                .where(getattr(self.model, identifier_field) == identifier_value)
                .values(**updated_fields)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()

            # Fetch the updated entity
            query = select(self.model).filter(getattr(self.model, identifier_field) == identifier_value)
            result = await session.execute(query)
            return result.scalars().first()
    
    async def delete(self, identifier_field: str, identifier_value: Any) -> bool:
        async with self.session as session:
            stmt = delete(self.model).where(getattr(self.model, identifier_field) == identifier_value)
            result = await session.execute(stmt)
            await session.commit()

            if result.rowcount == 0:  # Check if the delete operation affected any rows
                return False  # No rows deleted, record not found
            return True  # Rows deleted, deletion was successful

    async def get_all_by_where(self, params: GetAllByWhereGLB):
        sql = ""
        if params.where_conditions:
            if params.limit_range is not None and params.limit_range > 0:
                sql = f"SELECT * FROM {params.table_or_view_name} WHERE {params.where_conditions} ORDER BY {params.sort_column} LIMIT {params.limit_index}, {params.limit_range}"
            else:
                sql = f"SELECT * FROM {params.table_or_view_name} WHERE {params.where_conditions} ORDER BY {params.sort_column}"
        else:
            if params.limit_range is not None and params.limit_range > 0:
                sql = f"SELECT * FROM {params.table_or_view_name} ORDER BY {params.sort_column} LIMIT {params.limit_index}, {params.limit_range}"
            else:
                sql = f"SELECT * FROM {params.table_or_view_name} ORDER BY {params.sort_column}"

        print("qurey: ", sql)
        result = await self.session.execute(text(sql))
        return result.fetchall()
    
    async def count_all_by_where(self, params: CountByWhereGLB) -> int:
        if params.where_conditions:
            sql = f"SELECT COUNT({params.column_name}) AS TotalRecord FROM {params.table_or_view_name} WHERE {params.where_conditions}"
        else:
            sql = f"SELECT COUNT({params.column_name}) AS TotalRecord FROM {params.table_or_view_name}"

        result = await self.session.execute(text(sql))
        total_record = result.scalar()  # Get the first column of the first row
        return total_record