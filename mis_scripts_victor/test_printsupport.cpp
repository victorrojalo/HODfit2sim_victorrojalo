#include <QCoreApplication>
#include <QPrinter>
#include <QDebug>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QPrinter printer;
    printer.setPrinterName("TestPrinter");

    qDebug() << "[QtPrintSupport Test] Successfully created a fake QPrinter!";

    return 0;
}
