(ns editor
  (:import (javax.swing JFrame
                        JLabel
                        JTextField
                        JButton
                        JPanel
                        JTabbedPane)
           (java.awt GridLayout BorderLayout)
           (java.awt.event KeyEvent)
           #_(javax.swing.event *)))









(defn main []
  (let [frame (JFrame. "editor")
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





(main)





;; java -cp clojure-1.8.0.jar clojure.main editor.clj
