(defproject activitytools "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  

  :repositories ^:replace [["local"
                        {:url ~(str (.toURI (java.io.File. "jar")))
                        :checksum :warn}]]
            
  :dependencies [[jvtools/jvtools "1.0"]]
  :uberjar-name "activitytools.jar"
  :main activitytools.gui
  :aot [activitytools.gui]
  )

