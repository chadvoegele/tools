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
	val dir = "/home/chad/work/apma507_scans" //> dir  : String = /home/chad/work/apma507_scans
	val output = dir + "/" + "out.pdf"        //> output  : String = /home/chad/work/apma507_scans/out.pdf
	
	val filenames = convertScans.getImageFilenamesInDirectory(dir)
                                                  //> filenames  : List[String] = List(/home/chad/work/apma507_scans/out1-16.jpg, 
                                                  //| /home/chad/work/apma507_scans/out44-43.jpg, /home/chad/work/apma507_scans/ou
                                                  //| t1-28.jpg, /home/chad/work/apma507_scans/out1-26.jpg, /home/chad/work/apma50
                                                  //| 7_scans/out44-26.jpg, /home/chad/work/apma507_scans/out1-32.jpg, /home/chad/
                                                  //| work/apma507_scans/out44-32.jpg, /home/chad/work/apma507_scans/out1-43.jpg, 
                                                  //| /home/chad/work/apma507_scans/out44-8.jpg, /home/chad/work/apma507_scans/out
                                                  //| 44-19.jpg, /home/chad/work/apma507_scans/out1-11.jpg, /home/chad/work/apma50
                                                  //| 7_scans/out1-15.jpg, /home/chad/work/apma507_scans/out1-3.jpg, /home/chad/wo
                                                  //| rk/apma507_scans/out44-42.jpg, /home/chad/work/apma507_scans/out44-37.jpg, /
                                                  //| home/chad/work/apma507_scans/out44-13.jpg, /home/chad/work/apma507_scans/out
                                                  //| 44-7.jpg, /home/chad/work/apma507_scans/out44-22.jpg, /home/chad/work/apma50
                                                  //| 7_scans/out44-31.jpg, /home/chad/work/apma507_scans/out44-30.jpg, /home/chad
                                                  //| /work/apma507_scans/out4
                                                  //| Output exceeds cutoff limit.
	val blank_filenames = convertScans.getBlankFilenamesInDirectory(filenames)
                                                  //> blank_filenames  : Set[String] = Set(/home/chad/work/apma507_scans/out44-13.
                                                  //| jpg, /home/chad/work/apma507_scans/out1-35.jpg, /home/chad/work/apma507_scan
                                                  //| s/out44-2.jpg, /home/chad/work/apma507_scans/out44-25.jpg, /home/chad/work/a
                                                  //| pma507_scans/out44-12.jpg, /home/chad/work/apma507_scans/out44-16.jpg, /home
                                                  //| /chad/work/apma507_scans/out44-4.jpg, /home/chad/work/apma507_scans/out44-36
                                                  //| .jpg, /home/chad/work/apma507_scans/out44-35.jpg, /home/chad/work/apma507_sc
                                                  //| ans/out44-8.jpg, /home/chad/work/apma507_scans/out44-1.jpg, /home/chad/work/
                                                  //| apma507_scans/out44-5.jpg, /home/chad/work/apma507_scans/out44-21.jpg, /home
                                                  //| /chad/work/apma507_scans/out44-34.jpg, /home/chad/work/apma507_scans/out44-3
                                                  //| 3.jpg, /home/chad/work/apma507_scans/out44-40.jpg, /home/chad/work/apma507_s
                                                  //| cans/out1-43.jpg, /home/chad/work/apma507_scans/out44-43.jpg, /home/chad/wor
                                                  //| k/apma507_scans/out44-11.jpg, /home/chad/work/apma507_scans/out44-24.jpg, /h
                                                  //| ome/chad/work/apma507_sc
                                                  //| Output exceeds cutoff limit.
	val sortedFilenames = convertScans.sortFilenamesByScan(filenames)
                                                  //> sortedFilenames  : List[String] = List(/home/chad/work/apma507_scans/out1-1.
                                                  //| jpg, /home/chad/work/apma507_scans/out44-43.jpg, /home/chad/work/apma507_sca
                                                  //| ns/out1-2.jpg, /home/chad/work/apma507_scans/out44-42.jpg, /home/chad/work/a
                                                  //| pma507_scans/out1-3.jpg, /home/chad/work/apma507_scans/out44-41.jpg, /home/c
                                                  //| had/work/apma507_scans/out1-4.jpg, /home/chad/work/apma507_scans/out44-40.jp
                                                  //| g, /home/chad/work/apma507_scans/out1-5.jpg, /home/chad/work/apma507_scans/o
                                                  //| ut44-39.jpg, /home/chad/work/apma507_scans/out1-6.jpg, /home/chad/work/apma5
                                                  //| 07_scans/out44-38.jpg, /home/chad/work/apma507_scans/out1-7.jpg, /home/chad/
                                                  //| work/apma507_scans/out44-37.jpg, /home/chad/work/apma507_scans/out1-8.jpg, /
                                                  //| home/chad/work/apma507_scans/out44-36.jpg, /home/chad/work/apma507_scans/out
                                                  //| 1-9.jpg, /home/chad/work/apma507_scans/out44-35.jpg, /home/chad/work/apma507
                                                  //| _scans/out1-10.jpg, /home/chad/work/apma507_scans/out44-34.jpg, /home/chad/w
                                                  //| ork/apma507_scans/out1-1
                                                  //| Output exceeds cutoff limit.
  val sortedNonBlankFilenames = sortedFilenames.filter(x => !blank_filenames.contains(x))
                                                  //> sortedNonBlankFilenames  : List[String] = List(/home/chad/work/apma507_scans
                                                  //| /out1-1.jpg, /home/chad/work/apma507_scans/out1-2.jpg, /home/chad/work/apma5
                                                  //| 07_scans/out44-42.jpg, /home/chad/work/apma507_scans/out1-3.jpg, /home/chad/
                                                  //| work/apma507_scans/out44-41.jpg, /home/chad/work/apma507_scans/out1-4.jpg, /
                                                  //| home/chad/work/apma507_scans/out1-5.jpg, /home/chad/work/apma507_scans/out1-
                                                  //| 6.jpg, /home/chad/work/apma507_scans/out44-38.jpg, /home/chad/work/apma507_s
                                                  //| cans/out1-7.jpg, /home/chad/work/apma507_scans/out44-37.jpg, /home/chad/work
                                                  //| /apma507_scans/out1-8.jpg, /home/chad/work/apma507_scans/out1-9.jpg, /home/c
                                                  //| had/work/apma507_scans/out1-10.jpg, /home/chad/work/apma507_scans/out1-11.jp
                                                  //| g, /home/chad/work/apma507_scans/out1-12.jpg, /home/chad/work/apma507_scans/
                                                  //| out1-13.jpg, /home/chad/work/apma507_scans/out44-31.jpg, /home/chad/work/apm
                                                  //| a507_scans/out1-14.jpg, /home/chad/work/apma507_scans/out44-30.jpg, /home/ch
                                                  //| ad/work/apma507_scans/ou
                                                  //| Output exceeds cutoff limit./
  //val command = "convert " + sortedNonBlankFilenames.reduce((x, y) => x + " " + y) + " " + output
  //command.!!
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
		val explicitTrainNumber = 15;
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
	
	def sortFilenamesByScan(filenames : List[String]) : List[String] = {
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