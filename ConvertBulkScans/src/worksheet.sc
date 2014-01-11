import javax.swing._;
import javax.imageio.ImageIO;
import java.io.File;
import java.awt.image.BufferedImage;
import java.awt.Image;
import scala.sys.process._;
import scala.util._;
import java.util.ArrayList;
import scala.math._;
import weka._;

object test {
	val dir = "/home/chad/work/math5140"      //> dir  : String = /home/chad/work/math5140
	val output = dir + "/" + "math5140_doc.pdf"
                                                  //> output  : String = /home/chad/work/math5140/math5140_doc.pdf
	
	val filenames = convertScans.getImageFilenamesInDirectory(dir)
                                                  //> filenames  : List[String] = List(/home/chad/work/math5140/out93-1.jpg, /home
                                                  //| /chad/work/math5140/out1-55.jpg, /home/chad/work/math5140/out191-24.jpg, /ho
                                                  //| me/chad/work/math5140/out277-57.jpg, /home/chad/work/math5140/out191-8.jpg, 
                                                  //| /home/chad/work/math5140/out93-39.jpg, /home/chad/work/math5140/out191-29.jp
                                                  //| g, /home/chad/work/math5140/out191-80.jpg, /home/chad/work/math5140/out191-3
                                                  //| 7.jpg, /home/chad/work/math5140/out1-16.jpg, /home/chad/work/math5140/out277
                                                  //| -2.jpg, /home/chad/work/math5140/out277-61.jpg, /home/chad/work/math5140/out
                                                  //| 277-69.jpg, /home/chad/work/math5140/out1-28.jpg, /home/chad/work/math5140/o
                                                  //| ut277-13.jpg, /home/chad/work/math5140/out1-26.jpg, /home/chad/work/math5140
                                                  //| /out277-55.jpg, /home/chad/work/math5140/out277-78.jpg, /home/chad/work/math
                                                  //| 5140/out191-23.jpg, /home/chad/work/math5140/out277-50.jpg, /home/chad/work/
                                                  //| math5140/out191-32.jpg, /home/chad/work/math5140/out277-28.jpg, /home/chad/w
                                                  //| ork/math5140/out1-72.jpg
                                                  //| Output exceeds cutoff limit.
	val blank_filenames = convertScans.getBlankFilenamesInDirectory(filenames)
                                                  //> blank_filenames  : Set[String] = Set(/home/chad/work/math5140/out1-58.jpg, /
                                                  //| home/chad/work/math5140/out1-76.jpg, /home/chad/work/math5140/out1-14.jpg, /
                                                  //| home/chad/work/math5140/out93-10.jpg, /home/chad/work/math5140/out191-44.jpg
                                                  //| , /home/chad/work/math5140/out191-10.jpg, /home/chad/work/math5140/out93-6.j
                                                  //| pg, /home/chad/work/math5140/out191-27.jpg, /home/chad/work/math5140/out1-78
                                                  //| .jpg, /home/chad/work/math5140/out1-28.jpg, /home/chad/work/math5140/out1-68
                                                  //| .jpg, /home/chad/work/math5140/out1-48.jpg, /home/chad/work/math5140/out93-9
                                                  //| 2.jpg, /home/chad/work/math5140/out93-66.jpg, /home/chad/work/math5140/out19
                                                  //| 1-42.jpg, /home/chad/work/math5140/out1-84.jpg, /home/chad/work/math5140/out
                                                  //| 1-10.jpg, /home/chad/work/math5140/out1-92.jpg, /home/chad/work/math5140/out
                                                  //| 93-58.jpg, /home/chad/work/math5140/out1-86.jpg, /home/chad/work/math5140/ou
                                                  //| t191-72.jpg, /home/chad/work/math5140/out93-88.jpg, /home/chad/work/math5140
                                                  //| /out93-86.jpg, /home/cha
                                                  //| Output exceeds cutoff limit.
	//val sortedFilenames = convertScans.sortFilenamesBySingleSidedScan(filenames)
	val sortedFilenames = convertScans.sortFilenamesByDoubleSidedScan(filenames)
                                                  //> sortedFilenames  : List[String] = List(/home/chad/work/math5140/out1-1.jpg, 
                                                  //| /home/chad/work/math5140/out1-2.jpg, /home/chad/work/math5140/out1-3.jpg, /h
                                                  //| ome/chad/work/math5140/out1-4.jpg, /home/chad/work/math5140/out1-5.jpg, /hom
                                                  //| e/chad/work/math5140/out1-6.jpg, /home/chad/work/math5140/out1-7.jpg, /home/
                                                  //| chad/work/math5140/out1-8.jpg, /home/chad/work/math5140/out1-9.jpg, /home/ch
                                                  //| ad/work/math5140/out1-10.jpg, /home/chad/work/math5140/out1-11.jpg, /home/ch
                                                  //| ad/work/math5140/out1-12.jpg, /home/chad/work/math5140/out1-13.jpg, /home/ch
                                                  //| ad/work/math5140/out1-14.jpg, /home/chad/work/math5140/out1-15.jpg, /home/ch
                                                  //| ad/work/math5140/out1-16.jpg, /home/chad/work/math5140/out1-17.jpg, /home/ch
                                                  //| ad/work/math5140/out1-18.jpg, /home/chad/work/math5140/out1-19.jpg, /home/ch
                                                  //| ad/work/math5140/out1-20.jpg, /home/chad/work/math5140/out1-21.jpg, /home/ch
                                                  //| ad/work/math5140/out1-22.jpg, /home/chad/work/math5140/out1-23.jpg, /home/ch
                                                  //| ad/work/math5140/out1-24
                                                  //| Output exceeds cutoff limit.
  val sortedNonBlankFilenames = sortedFilenames.filter(x => !blank_filenames.contains(x))
                                                  //> sortedNonBlankFilenames  : List[String] = List(/home/chad/work/math5140/out1
                                                  //| -1.jpg, /home/chad/work/math5140/out1-2.jpg, /home/chad/work/math5140/out1-3
                                                  //| .jpg, /home/chad/work/math5140/out1-5.jpg, /home/chad/work/math5140/out1-6.j
                                                  //| pg, /home/chad/work/math5140/out1-7.jpg, /home/chad/work/math5140/out1-8.jpg
                                                  //| , /home/chad/work/math5140/out1-9.jpg, /home/chad/work/math5140/out1-11.jpg,
                                                  //|  /home/chad/work/math5140/out1-13.jpg, /home/chad/work/math5140/out1-15.jpg,
                                                  //|  /home/chad/work/math5140/out1-16.jpg, /home/chad/work/math5140/out1-17.jpg,
                                                  //|  /home/chad/work/math5140/out1-19.jpg, /home/chad/work/math5140/out1-21.jpg,
                                                  //|  /home/chad/work/math5140/out1-22.jpg, /home/chad/work/math5140/out1-23.jpg,
                                                  //|  /home/chad/work/math5140/out1-25.jpg, /home/chad/work/math5140/out1-26.jpg,
                                                  //|  /home/chad/work/math5140/out1-27.jpg, /home/chad/work/math5140/out1-29.jpg,
                                                  //|  /home/chad/work/math5140/out1-31.jpg, /home/chad/work/math5140/out1-33.jpg,
                                                  //|  /home/chad/work/math514
                                                  //| Output exceeds cutoff limit.
  val sortedNonBlankPDFFilenames = sortedNonBlankFilenames.map(x => x.replaceAll("[.]jpg", ".pdf"))
                                                  //> sortedNonBlankPDFFilenames  : List[String] = List(/home/chad/work/math5140/o
                                                  //| ut1-1.pdf, /home/chad/work/math5140/out1-2.pdf, /home/chad/work/math5140/out
                                                  //| 1-3.pdf, /home/chad/work/math5140/out1-5.pdf, /home/chad/work/math5140/out1-
                                                  //| 6.pdf, /home/chad/work/math5140/out1-7.pdf, /home/chad/work/math5140/out1-8.
                                                  //| pdf, /home/chad/work/math5140/out1-9.pdf, /home/chad/work/math5140/out1-11.p
                                                  //| df, /home/chad/work/math5140/out1-13.pdf, /home/chad/work/math5140/out1-15.p
                                                  //| df, /home/chad/work/math5140/out1-16.pdf, /home/chad/work/math5140/out1-17.p
                                                  //| df, /home/chad/work/math5140/out1-19.pdf, /home/chad/work/math5140/out1-21.p
                                                  //| df, /home/chad/work/math5140/out1-22.pdf, /home/chad/work/math5140/out1-23.p
                                                  //| df, /home/chad/work/math5140/out1-25.pdf, /home/chad/work/math5140/out1-26.p
                                                  //| df, /home/chad/work/math5140/out1-27.pdf, /home/chad/work/math5140/out1-29.p
                                                  //| df, /home/chad/work/math5140/out1-31.pdf, /home/chad/work/math5140/out1-33.p
                                                  //| df, /home/chad/work/math
                                                  //| Output exceeds cutoff limit.
  val convertToPDF = sortedNonBlankFilenames.zip(sortedNonBlankPDFFilenames).map({case (x, y) => "convert " + x + " " + y})
                                                  //> convertToPDF  : List[String] = List(convert /home/chad/work/math5140/out1-1.
                                                  //| jpg /home/chad/work/math5140/out1-1.pdf, convert /home/chad/work/math5140/ou
                                                  //| t1-2.jpg /home/chad/work/math5140/out1-2.pdf, convert /home/chad/work/math51
                                                  //| 40/out1-3.jpg /home/chad/work/math5140/out1-3.pdf, convert /home/chad/work/m
                                                  //| ath5140/out1-5.jpg /home/chad/work/math5140/out1-5.pdf, convert /home/chad/w
                                                  //| ork/math5140/out1-6.jpg /home/chad/work/math5140/out1-6.pdf, convert /home/c
                                                  //| had/work/math5140/out1-7.jpg /home/chad/work/math5140/out1-7.pdf, convert /h
                                                  //| ome/chad/work/math5140/out1-8.jpg /home/chad/work/math5140/out1-8.pdf, conve
                                                  //| rt /home/chad/work/math5140/out1-9.jpg /home/chad/work/math5140/out1-9.pdf, 
                                                  //| convert /home/chad/work/math5140/out1-11.jpg /home/chad/work/math5140/out1-1
                                                  //| 1.pdf, convert /home/chad/work/math5140/out1-13.jpg /home/chad/work/math5140
                                                  //| /out1-13.pdf, convert /home/chad/work/math5140/out1-15.jpg /home/chad/work/m
                                                  //| ath5140/out1-15.pdf, con
                                                  //| Output exceeds cutoff limit.
  convertToPDF.map(x => x.!!)                     //> res0: List[String] = List("", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                                                  //| , "", "", "", "", "", ""
                                                  //| Output exceeds cutoff limit.
  val command = "pdfunite " + sortedNonBlankPDFFilenames.reduce((x, y) => x + " " + y) + " " + output
                                                  //> command  : String = pdfunite /home/chad/work/math5140/out1-1.pdf /home/chad
                                                  //| /work/math5140/out1-2.pdf /home/chad/work/math5140/out1-3.pdf /home/chad/wo
                                                  //| rk/math5140/out1-5.pdf /home/chad/work/math5140/out1-6.pdf /home/chad/work/
                                                  //| math5140/out1-7.pdf /home/chad/work/math5140/out1-8.pdf /home/chad/work/mat
                                                  //| h5140/out1-9.pdf /home/chad/work/math5140/out1-11.pdf /home/chad/work/math5
                                                  //| 140/out1-13.pdf /home/chad/work/math5140/out1-15.pdf /home/chad/work/math51
                                                  //| 40/out1-16.pdf /home/chad/work/math5140/out1-17.pdf /home/chad/work/math514
                                                  //| 0/out1-19.pdf /home/chad/work/math5140/out1-21.pdf /home/chad/work/math5140
                                                  //| /out1-22.pdf /home/chad/work/math5140/out1-23.pdf /home/chad/work/math5140/
                                                  //| out1-25.pdf /home/chad/work/math5140/out1-26.pdf /home/chad/work/math5140/o
                                                  //| ut1-27.pdf /home/chad/work/math5140/out1-29.pdf /home/chad/work/math5140/ou
                                                  //| t1-31.pdf /home/chad/work/math5140/out1-33.pdf /home/chad/work/math5140/out
                                                  //| 1-35.pdf /home/chad/wor
                                                  //| Output exceeds cutoff limit.
  command.!!                                      //> res1: String = ""
}

object convertScans {
	def isImageBlankExplicit(filename : String) : Boolean  = {
		val img = ImageIO.read(new File(filename));
	  val scaled_img = img.getScaledInstance(img.getWidth() / 4, img.getHeight() / 4, Image.SCALE_SMOOTH);
	  val icon = new ImageIcon(scaled_img)
		val opts : Array[Object] = Array("Yes", "No")
		val n = JOptionPane.showOptionDialog(null, "Is blank?", "Is blank?",
			 JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE, icon, opts, opts(0));
		return n == 0
	}
	
	def getImageStandardDeviations(filenames : List[String]) : List[Double] = {
		val identify_cmd = "identify -format %[standard-deviation]\\n " + filenames.reduceLeft((x, y) => x + " " + y)
	  return identify_cmd.!!.split("\n").toList.map(x => x.toDouble)
	}
	
	def getImageFilenamesInDirectory(dir : String) : List[String] =
		return new File(dir).listFiles.map(x => x.getPath).filter(x => x.endsWith(".jpg")).toList
		
	def getProbOfBlank(train_data : List[(Double, Boolean)], all_stdev : List[Double]) : List[Double] = {
	  var atts = new ArrayList[weka.core.Attribute]();
	  var ignore = atts.add(new weka.core.Attribute("stdev"));
	  var nom = new ArrayList[String]();
	  ignore = nom.add("notblank");
	  ignore = nom.add("blank");
	  ignore = atts.add(new weka.core.Attribute("isblank", nom));
				
	  var train_instances = new weka.core.Instances("myRelation", atts, 0);
		for (i <- 0 until train_data.length) {
			train_data(i) match {
				case (stdev, isblank) => {
					if (isblank)
						train_instances.add(new weka.core.DenseInstance(1.0, Array(stdev, 0.0)));
					else
						train_instances.add(new weka.core.DenseInstance(1.0, Array(stdev, 1.0)));
				}
			}
		}
		train_instances.setClassIndex(train_instances.numAttributes() - 1);
	  
		var lr = new weka.classifiers.functions.Logistic()
		lr.buildClassifier(train_instances);
	  var data = new weka.core.Instances("myRelation", atts, 0);
	  
	  all_stdev.map(x => data.add(new weka.core.DenseInstance(1.0, Array(x, 0.0))));
	  data.setClassIndex(data.numAttributes() - 1);
	  
	  return (0 until all_stdev.length).map(i => lr.distributionForInstance(data.get(i))(0)).toList;
	}
	
	def getBlankFilenamesInDirectory(filenames : List[String]) : Set[String] = {
		val explicitTrainNumber = 20;
		val explicitTrainProbLower = 0.01
		
		val stdevs = convertScans.getImageStandardDeviations(filenames)
		val objs = filenames.zip(stdevs).map({case (x, y) => new imageData(x, y)})
	  val num_explicit_train = min(explicitTrainNumber, objs.length)
	  val objs_shuffle = Random.shuffle(objs.toList)
	  val objs_train = objs_shuffle.take(num_explicit_train)
	  val objs_skip = objs_shuffle.drop(num_explicit_train)
		val explicit_blank = objs_train.map(x => convertScans.isImageBlankExplicit(x.filename))
		val explicit_train_objs = objs_train.zip(explicit_blank).map({case (x, y) => new imageData(x.filename, x.stdDev, Some(y))})
		val objs2 = objs_skip ++ explicit_train_objs
		val train_data = objs2.filter(x => x.isBlankExplicit.isDefined).map(x => (x.stdDev, x.isBlankExplicit.getOrElse(false)))
	  val all_stdevs = objs2.map(x => x.stdDev)
	  val probs = convertScans.getProbOfBlank(train_data, all_stdevs)
	  val obj3 = objs2.zip(probs).map({case (x, y) => new imageData(x.filename, x.stdDev, x.isBlankExplicit, Some(y))})
		val objs4blankmiddle = obj3.filter(x => x.probBlank.getOrElse(.5) >= explicitTrainProbLower && x.probBlank.getOrElse(.5) <= 1-explicitTrainProbLower)
	  val isblankmiddle = objs4blankmiddle.map(x => convertScans.isImageBlankExplicit(x.filename))
		val objs5_blankmiddle = objs4blankmiddle.zip(isblankmiddle).map({case (x, y) => new imageData(x.filename, x.stdDev, Some(y), x.probBlank)})
		val objs5 = objs5_blankmiddle ++ obj3.filter(x => !(x.probBlank.getOrElse(.5) >= explicitTrainProbLower && x.probBlank.getOrElse(.5) <= 1-explicitTrainProbLower))
	  val objs6 = objs5.filter(x => x.isBlank);
		return objs6.map(x => x.filename).toSet
	}
	
	def sortFilenamesBySingleSidedScan(filenames : List[String]) : List[String] = {
		val filenameMap = filenames.groupBy(x => x.drop(x.indexOfSlice("out") + 3).take(x.indexOfSlice("-") - x.indexOfSlice("out") - 3).toInt)
		val keys = filenameMap.keySet.toList.sortBy(x =>  x)
		
		var lst : List[String] = Nil
		
		for (i <- 0 until keys.length by 2) {
			val frontkey = keys.apply(i)
			val backkey = keys.apply(i+1)
			val frontfilenames = filenameMap(frontkey).sortBy(x => x.drop(x.indexOfSlice("-") + 1).take(x.indexOfSlice(".jpg") - x.indexOfSlice("-") - 1).toInt)
			val backfilenames = filenameMap(backkey).sortBy(x => x.drop(x.indexOfSlice("-") + 1).take(x.indexOfSlice(".jpg") - x.indexOfSlice("-") - 1).toInt).reverse
			lst = lst ++ frontfilenames.zip(backfilenames).map({case (x, y) => x :: y :: Nil}).flatten
		}
		
		return lst
	}
	
	def sortFilenamesByDoubleSidedScan(filenames : List[String]) : List[String] = {
		val filenameMap = filenames.groupBy(x => x.drop(x.indexOfSlice("out") + 3).take(x.indexOfSlice("-") - x.indexOfSlice("out") - 3).toInt)
		val keys = filenameMap.keySet.toList.sortBy(x =>  x)
		return keys.map(k => filenameMap(k).sortBy(x => x.drop(x.indexOfSlice("-") + 1).take(x.indexOfSlice(".jpg") - x.indexOfSlice("-") - 1).toInt)).flatten
	}
}

class imageData(val filename: String,
	val stdDev: Double,
	val isBlankExplicit : Option[Boolean] = None,
	val probBlank : Option[Double]= None) {
	
	def isBlank() : Boolean = {
		isBlankExplicit match {
			case Some(x) => return x
			case None => probBlank match {
				case Some(x) =>
					if (x >= 0.5)
						return true
					else
						return false
			}
		}
		return false
	}
	override def toString(): String =
		return "[" + filename + " " + stdDev.toString + " " + isBlankExplicit.toString + " " + probBlank.toString + "]"
}