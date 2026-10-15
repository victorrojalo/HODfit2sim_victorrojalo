#include <QApplication>
#include <QOpenGLWidget>

class MyGLWidget : public QOpenGLWidget {
public:
    bool m_initialized = false;
protected:
    void initializeGL() override {
        qDebug() << "[QtOpenGLWidgets Test] OpenGL initialized!";
        m_initialized = true;
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    MyGLWidget w;
    w.resize(200, 200);
    w.show();

    if(!w.m_initialized) {
        return 1;
    }

    return 0;
}
