#include <QCoreApplication>
#include <QtConcurrent>
#include <QDebug>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QFuture<QString> future = QtConcurrent::run([]() {
        return QString("[QtConcurrent Test] Concurrent task done!");
    });

    QFutureWatcher<QString> watcher;

    QObject::connect(&watcher, &QFutureWatcher<QString>::finished, [&]() {
        qDebug() << future.result();
        app.quit();
    });

    watcher.setFuture(future);

    return app.exec();
}
