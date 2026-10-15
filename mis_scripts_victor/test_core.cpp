#include <QCoreApplication>
#include <QTimer>
#include <QDebug>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);
    QTimer::singleShot(100, []() {
        qDebug() << "[QtCore Test] QtCore works!";
        QCoreApplication::quit();
    });
    return app.exec();
}
