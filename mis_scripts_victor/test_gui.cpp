#include <QGuiApplication>
#include <QFont>
#include <QDebug>

int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);

    QFont font("Arial", 10);
    qDebug() << "[QtGui Test] QtGui loaded font:" << font.family();

    return 0;
}
