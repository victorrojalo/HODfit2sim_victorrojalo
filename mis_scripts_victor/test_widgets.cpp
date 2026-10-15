#include <QApplication>
#include <QPushButton>
#include <QDebug>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QPushButton btn("I am a button");
    qDebug() << "[QtWidgets Test] Successfully created QPushButton:" << btn.text();

    return 0;
}
