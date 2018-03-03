(ns activitytools.gui
  (:gen-class)
  (:import (javax.swing JFrame
                        JLabel
                        JTextField
                        JButton
                        JPanel
                        JTabbedPane
                        JTextArea
                        JComboBox
                        JFileChooser
                        JScrollPane
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
            [activitytools.control :refer :all]
            ))



(defn Button-check [text1 text2 text3 text4]
  (proxy [JButton ActionListener][]
    (actionPerformed [e]
      (let [prop_separators (string/trim (.getText text1))
            propnum_separators (string/trim (.getText text2))
            props (string/trim (.getText text3))]
        (if (some empty?
                  [prop_separators
                   propnum_separators
                   props])
          (JOptionPane/showMessageDialog nil "内容不能为空！")
          (.setText text4 (string/join "\n" (make_props
                                             prop_separators
                                             propnum_separators
                                             props))))))))

(defn get-panel1 []
  (let* [panelback (JPanel.)
         panel (JPanel.)
         label1 (JLabel. "道具分隔符")
         label2 (JLabel. "数量分隔符")
         text1 (JTextField. "，|、|,")
         text2 (JTextField. "*|×|x")
         text3 (JTextField. "")
         text4 (JTextArea.)
         button (Button-check text1 text2 text3 text4) 
         scrolltext (JScrollPane. text4)]
    (doto button
      (.setText "查询")
      (.addActionListener button))
    (doto panel
      (.setLayout (GridLayout. 0 1))
      (.add label1)
      (.add text1)
      (.add label2)
      (.add text2)
      (.add text3)
      (.add button))
    (doto panelback
      (.setLayout (BorderLayout.))
      (.add panel BorderLayout/NORTH)
      (.add scrolltext BorderLayout/CENTER))
    panelback))

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
            (let [save-file-path (.getPath (io/file
                                            (.getAbsolutePath (.getSelectedFile fc))
                                            (str (.getText text) ".xml")))]
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
      (.setLayout (GridLayout. 0 1))
      (.add label1)
      (.add button)
      (.add text-ms)
      (.add button-ms)
      (.add text-qq)
      (.add button-qq)) 
    panel))

(defn Button-gm-new-servers [gametype startid endid]
  (proxy [JButton ActionListener][]
    (actionPerformed [e]
      (let* [gametype ({0 "s" 1 "m"} (.getSelectedIndex gametype))
             startid (try (Integer/parseInt (.getText startid))
                          (catch Exception e -1))
             endid (try (Integer/parseInt (.getText endid))
                        (catch Exception e -1))]
        (if (and (> startid 0)
                 (> endid 0)
                 (>= endid startid))
          (let [content (get-gm-new-servers gametype startid endid)
                fc (doto (JFileChooser.)
                     (.setDialogType JFileChooser/SAVE_DIALOG)
                     (.setFileSelectionMode JFileChooser/DIRECTORIES_ONLY))
                ret (.showDialog fc nil "保存文件")]
            (if (= ret JFileChooser/APPROVE_OPTION) 
              (let [save-file-path (.getPath (io/file
                                              (.getAbsolutePath (.getSelectedFile fc))
                                              (format "%s%d-%d.txt" gametype startid endid)))]
                (if content
                  (spit save-file-path content)
                  (JOptionPane/showMessageDialog nil "获取失败！")))))
          (JOptionPane/showMessageDialog nil "请输入正确的id！"))))))

(defn get-panel3 []
  (let* [panel (JPanel.)
         label1 (JLabel. "游戏类型")
         combobox (JComboBox.)
         label2 (JLabel. "开始id")
         text1 (JTextField. "")
         label3 (JLabel. "结束id")
         text2 (JTextField. "")
         button (Button-gm-new-servers combobox text1 text2)]
    (doto combobox
      (.addItem "幻三")
      (.addItem "梦三"))
    (doto button
      (.setText "获取")
      (.addActionListener button))
    (doto panel
      (.setLayout (GridLayout. 0 1))
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
      (.add panel3 "gm新服"))
    (doto frame
      (.setDefaultCloseOperation
       (JFrame/EXIT_ON_CLOSE))
      (.setSize 600 500)
      (.setLocationRelativeTo nil)
      (.setLayout (BorderLayout.))
      (.add tabs BorderLayout/CENTER)
      (.setVisible true))))

(defn -main [& args]
  (gui))


