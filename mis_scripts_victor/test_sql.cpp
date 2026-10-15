#include <QCoreApplication>
#include <QtSql>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(":memory:");

    if (db.open()) {
        QSqlQuery q;
        q.exec("CREATE TABLE test (id INTEGER, name TEXT)");
        q.exec("INSERT INTO test VALUES (1, 'Alice')");
        q.exec("SELECT name FROM test");
        if (q.next()) {
            qDebug() << "[QtSql Test] SQL result: " << q.value(0).toString();
        }
    } else {
        qDebug() << "[QtSql Test] Failed to open DB!";
        return 1;
    }

    return 0;
}
