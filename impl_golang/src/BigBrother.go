package lib

import (
	"io/ioutil"
	"log"
	"os"
)

func getFileList(path string) (files []string) {
	var dirs []string
	separator := string(os.PathSeparator)
	dir, err := ioutil.ReadDir(path)
	if err != nil {
		log.Fatalln(err)
	}
	for _, fi := range dir {
		if fi.IsDir() {
			dirs = append(dirs, path+separator+fi.Name())
			getFileList(path + separator + fi.Name())
		} else {
			files = append(files, path+separator+fi.Name())
		}
	}
	return files
}
