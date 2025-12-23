mermaid
graph TD

subgraph Client ["クライアント層"]
    User["👤 利用者（社員）<br/>Webブラウザ"]
end

subgraph AppServer ["Web / Application層"]
    Flask["Python (Flask)"]
    Logic["・備品一覧表示 (Read)<br/>・備品登録 (Create)<br/>・備品更新 (Update)<br/>・備品削除 (Delete)<br/>・業務ロジック処理"]
end

subgraph DBServer ["DBサーバ層"]
    Postgres["PostgreSQL (RDB)"]
    Table["items テーブル<br/>・id<br/>・name<br/>・quantity<br/>・status"]
end

User -- "HTTP / HTTPS" --> Flask
Flask --- Logic
Logic -- "SQLAlchemy" --> Postgres
Postgres --- Table

style Client fill:#f9f9f9,stroke:#333
style AppServer fill:#e1f5fe,stroke:#01579b
style DBServer fill:#e8f5e9,stroke:#1b5e20
