
(ns demos
  (:import (javax.swing JFrame
                        JLabel
                        JTextField
                        JButton
                        JPanel
                        JTabbedPane
                        JScrollPane
                        JTextArea)
           (java.awt GridLayout BorderLayout)
           (java.awt.event KeyEvent
                           KeyListener
                           WindowEvent
                           ActionListener)
           #_(javax.swing.event *)))









(defn make-tabs []
  (let [frame (JFrame. "demos")
        tabs (JTabbedPane. JTabbedPane/TOP)
        panel1 (JPanel.)
        panel2 (JPanel.)
        ]
    (doto tabs
      (.add panel1 "first")
      (.setMnemonicAt 0 KeyEvent/VK_0)
      (.add panel2 "second")
      (.setMnemonicAt 1 KeyEvent/VK_1)
      )
    (doto frame
      (.setDefaultCloseOperation
       (JFrame/EXIT_ON_CLOSE))
      (.setSize 300 200)
      (.setLayout (BorderLayout.))
      (.add tabs BorderLayout/CENTER)
      (.setVisible true))))


(defn Text []
  (proxy [JTextArea KeyListener][]
    (keyPressed [e]
      (doto this
        (.append (KeyEvent/getKeyText (.getKeyCode e)))))
    (keyReleased [e]
      (print "shit"))
    (keyTyped [e]
      (print "shit"))))


(defn make-event []
  (let [frame (JFrame. "demos")
        text (Text)]
    
    #_(doto panel
      (.setBounds 5 5 300 200)
      (.addKeyListener panel)
      )

    (doto text
      (.addKeyListener text))

    (doto frame
      (.setDefaultCloseOperation
       (JFrame/EXIT_ON_CLOSE))
      (.setSize 300 200)
      (.add text)
      (.setVisible true))))

(defn Button [text]
  (proxy [JButton ActionListener][]
      (actionPerformed [e]
                       (doto text
                         (.setText "yes")))))

(defn make-button-event []
  (let* [frame (JFrame. "demos")
        text (JTextField.)
        button (Button text)]

    (doto button
      (.setText "确定")
      (.addActionListener button))


    (doto frame
      (.setDefaultCloseOperation
       (JFrame/EXIT_ON_CLOSE))
      (.setSize 300 200)
      (.setLayout (BorderLayout.))
      (.add text BorderLayout/NORTH)
      (.add button BorderLayout/CENTER)
      (.setVisible true))))

((fn []
   ;; (make-tabs)
   ;; (make-event)
   (make-button-event)
  ))





;; java -cp clojure-1.8.0.jar clojure.main demos.clj



