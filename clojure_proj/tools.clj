
(ns tools
  (:import (javax.swing JFrame
                        JLabel
                        JTextField
                        JButton
                        JPanel
                        JTabbedPane
                        JTextArea
                        JComboBox
                        JFileChooser
                        JOptionPane)
           (java.awt GridLayout
                     BorderLayout
                     FlowLayout
                     GridBagLayout
                     GridBagConstraints)
           (java.awt.event KeyEvent
                           ActionListener))
  (:require [clojure.string :as string]
            [clojure.java.io :as io] 
            [control :refer :all]
            ))



(defn Button-check [text1 text2 text3 text4]
  (proxy [JButton ActionListener][]
    (actionPerformed [e]
      (.setText text4 (string/join "\n" (make_props
                                      (.getText text1)
                                      (.getText text2)
                                      (.getText text3)))))))


(defn get-panel1 []
  (let* [panel (JPanel.)
         label1 (JLabel. "道具分隔符")
         label2 (JLabel. "数量分隔符")
         text1 (JTextField. "，|、|,")
         text2 (JTextField. "*|×|x")
         text3 (JTextField. "宝石25×15，紅鑽石30×2，藍鑽石30×8，黃鑽石30×6，未知30×4，未知30+6")
         text4 (JTextArea.)
         button (Button-check text1 text2 text3 text4) 
         c (GridBagConstraints.)]
    (doto button
      (.setText "查询")
      (.addActionListener button))
    (doto panel
      (.setLayout (GridLayout. 7 1))
      (.add label1)
      (.add text1)
      (.add label2)
      (.add text2)
      (.add text3)
      (.add button)
      (.add text4))
    panel))

(defn Button-choose-file [label]
  (proxy [JButton ActionListener][]
    (actionPerformed [e]
      (let* [fc (JFileChooser.)
            ret (.showDialog fc nil "请选择文件")]
        (if (= ret JFileChooser/APPROVE_OPTION)
          (.setText label (.getAbsolutePath
                           (.getSelectedFile fc))))))))

(defn Button-save [label text trans_type]
  (proxy [JButton ActionListener][]
    (actionPerformed [e]
      (if (and (or (not (empty? (.getText label)))
                   (JOptionPane/showMessageDialog nil "请先选择文件！"))
               (or (not (empty? (.getText text))) 
                   (JOptionPane/showMessageDialog nil "文件名不能为空！")))
        (let* [fc (doto (JFileChooser.)
                    (.setDialogType JFileChooser/SAVE_DIALOG)
                    (.setFileSelectionMode JFileChooser/DIRECTORIES_ONLY))
               ret (.showDialog fc nil "保存文件")]
          (if (= ret JFileChooser/APPROVE_OPTION) 
            (let [save-file-path (.getPath (io/file (.getAbsolutePath (.getSelectedFile fc))
                                                    (.getText text)))]
              (with-open [rf (io/reader (.getText label))]
                (let [content (string/join "\n" (hs2ms2qq (line-seq rf) trans_type))]
                  (spit save-file-path content))))))))))

(defn get-panel2 []
  (let* [panel (JPanel.)
         label1 (JLabel.)
         button (Button-choose-file label1)
         text-ms (JTextField.)
         button-ms (Button-save label1 text-ms "hs2ms")
         text-qq (JTextField.)
         button-qq (Button-save label1 text-qq "hs2qq")]
    (doto button
      (.setText "选择文件")
      (.addActionListener button))
    (doto button-ms
      (.setText "转梦三")
      (.addActionListener button-ms))
    (doto button-qq
      (.setText "转魔三")
      (.addActionListener button-qq))
    (doto panel
      (.setLayout (GridLayout. 6 1))
      (.add label1)
      (.add button)
      (.add text-ms)
      (.add button-ms)
      (.add text-qq)
      (.add button-qq))
    #_(doto fc
        (.showDialog nil "请选择文件"))
    panel))

(defn Button-gm-new-servers [gametype startid endid]
  (proxy [JButton ActionListener][]
    (actionPerformed [e]
      (let* [gametype ({0 "s" 1 "m"} (.getSelectedIndex gametype))
             startid (Integer/parseInt (.getText startid))
             endid (Integer/parseInt (.getText endid))
             content (get-gm-new-servers gametype startid endid)
             fc (doto (JFileChooser.)
                  (.setDialogType JFileChooser/SAVE_DIALOG)
                  (.setFileSelectionMode JFileChooser/DIRECTORIES_ONLY))
             ret (.showDialog fc nil "保存文件")]
        (if (= ret JFileChooser/APPROVE_OPTION) 
          (let [save-file-path (.getPath (io/file
                                          (.getAbsolutePath (.getSelectedFile fc))
                                          (format "%s%d-%d.txt" gametype startid endid)))]
            (spit save-file-path content)))))))

(defn get-panel3 []
  (let* [panel (JPanel.)
         label1 (JLabel. "游戏类型")
         combobox (JComboBox.)
         label2 (JLabel. "开始id")
         text1 (JTextField. "15")
         label3 (JLabel. "结束id")
         text2 (JTextField. "20")
         button (Button-gm-new-servers combobox text1 text2)]
    (doto combobox
      (.addItem "幻三")
      (.addItem "梦三"))
    (doto button
      (.setText "获取")
      (.addActionListener button))
    (doto panel
      (.setLayout (GridLayout. 7 1))
      (.add label1)
      (.add combobox)
      (.add label2)
      (.add text1)
      (.add label3)
      (.add text2)
      (.add button))
    panel))

(defn gui []
  (let [frame (JFrame. "tools")
        tabs (JTabbedPane. JTabbedPane/TOP)
        panel1 (get-panel1)
        panel2 (get-panel2)
        panel3 (get-panel3)]
    (doto tabs
      (.add panel1 "道具查询")
      (.add panel2 "配置转换")
      (.add panel3 "gm新服")
      )
    (doto frame
      (.setDefaultCloseOperation
       (JFrame/EXIT_ON_CLOSE))
      (.setSize 600 400)
      (.setLayout (BorderLayout.))
      (.add tabs BorderLayout/CENTER)
      (.setVisible true))))

(gui)

;; java -cp ./;clojure-1.8.0.jar;jsch-0.1.54.jar clojure.main tools.clj
;; java -classpath ./;clojure-1.8.0.jar;jsch-0.1.54.jar clojure.main tools.clj

