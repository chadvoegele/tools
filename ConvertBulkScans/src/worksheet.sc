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
	val explicitTrainNumber = 5;              //> explicitTrainNumber  : Int = 5
	val explicitTrainProbLower = 0.3          //> explicitTrainProbLower  : Double = 0.3
	val filenames = convertScans.getImageFilenamesInDirectory("/home/chad/work/apma507_scans").take(10)
                                                  //> filenames  : Array[String] = Array(/home/chad/work/apma507_scans/out44-37.jp
                                                  //| g, /home/chad/work/apma507_scans/out1-17.jpg, /home/chad/work/apma507_scans/
                                                  //| out1-25.jpg, /home/chad/work/apma507_scans/out1-38.jpg, /home/chad/work/apma
                                                  //| 507_scans/out1-9.jpg, /home/chad/work/apma507_scans/out1-34.jpg, /home/chad/
                                                  //| work/apma507_scans/out44-15.jpg, /home/chad/work/apma507_scans/out44-10.jpg,
                                                  //|  /home/chad/work/apma507_scans/out44-27.jpg, /home/chad/work/apma507_scans/o
                                                  //| ut44-4.jpg)
	val stdevs = convertScans.getImageStandardDeviations(filenames.toList)
                                                  //> stdevs  : List[Double] = List(9401.1, 7549.48, 11239.1, 12122.6, 8369.6, 765
                                                  //| 5.92, 8194.47, 3695.97, 7581.85, 4195.3)
	val objs = filenames.zip(stdevs).map({case (x, y) => new imageData(x, y)})
                                                  //> objs  : Array[imageData] = Array([/home/chad/work/apma507_scans/out44-37.jpg
                                                  //|  9401.1 None None], [/home/chad/work/apma507_scans/out1-17.jpg 7549.48 None 
                                                  //| None], [/home/chad/work/apma507_scans/out1-25.jpg 11239.1 None None], [/home
                                                  //| /chad/work/apma507_scans/out1-38.jpg 12122.6 None None], [/home/chad/work/ap
                                                  //| ma507_scans/out1-9.jpg 8369.6 None None], [/home/chad/work/apma507_scans/out
                                                  //| 1-34.jpg 7655.92 None None], [/home/chad/work/apma507_scans/out44-15.jpg 819
                                                  //| 4.47 None None], [/home/chad/work/apma507_scans/out44-10.jpg 3695.97 None No
                                                  //| ne], [/home/chad/work/apma507_scans/out44-27.jpg 7581.85 None None], [/home/
                                                  //| chad/work/apma507_scans/out44-4.jpg 4195.3 None None])
  val num_explicit_train = min(explicitTrainNumber, objs.length)
                                                  //> num_explicit_train  : Int = 5
  val objs_shuffle = Random.shuffle(objs.toList)  //> objs_shuffle  : List[imageData] = List([/home/chad/work/apma507_scans/out44-
                                                  //| 15.jpg 8194.47 None None], [/home/chad/work/apma507_scans/out1-34.jpg 7655.9
                                                  //| 2 None None], [/home/chad/work/apma507_scans/out44-27.jpg 7581.85 None None]
                                                  //| , [/home/chad/work/apma507_scans/out44-37.jpg 9401.1 None None], [/home/chad
                                                  //| /work/apma507_scans/out44-4.jpg 4195.3 None None], [/home/chad/work/apma507_
                                                  //| scans/out1-25.jpg 11239.1 None None], [/home/chad/work/apma507_scans/out1-17
                                                  //| .jpg 7549.48 None None], [/home/chad/work/apma507_scans/out44-10.jpg 3695.97
                                                  //|  None None], [/home/chad/work/apma507_scans/out1-9.jpg 8369.6 None None], [/
                                                  //| home/chad/work/apma507_scans/out1-38.jpg 12122.6 None None])
  val objs_train = objs_shuffle.take(num_explicit_train)
                                                  //> objs_train  : List[imageData] = List([/home/chad/work/apma507_scans/out44-15
                                                  //| .jpg 8194.47 None None], [/home/chad/work/apma507_scans/out1-34.jpg 7655.92 
                                                  //| None None], [/home/chad/work/apma507_scans/out44-27.jpg 7581.85 None None], 
                                                  //| [/home/chad/work/apma507_scans/out44-37.jpg 9401.1 None None], [/home/chad/w
                                                  //| ork/apma507_scans/out44-4.jpg 4195.3 None None])
  val objs_skip = objs_shuffle.drop(num_explicit_train)
                                                  //> objs_skip  : List[imageData] = List([/home/chad/work/apma507_scans/out1-25.j
                                                  //| pg 11239.1 None None], [/home/chad/work/apma507_scans/out1-17.jpg 7549.48 No
                                                  //| ne None], [/home/chad/work/apma507_scans/out44-10.jpg 3695.97 None None], [/
                                                  //| home/chad/work/apma507_scans/out1-9.jpg 8369.6 None None], [/home/chad/work/
                                                  //| apma507_scans/out1-38.jpg 12122.6 None None])
	val explicit_blank = objs_train.map(x => convertScans.isImageBlankExplicit(x.filename))
                                                  //> explicit_blank  : List[Boolean] = List(false, false, false, false, true)
	val explicit_train_objs = objs_train.zip(explicit_blank).map({case (x, y) => new imageData(x.filename, x.stdDev, Some(y))})
                                                  //> explicit_train_objs  : List[imageData] = List([/home/chad/work/apma507_scan
                                                  //| s/out44-15.jpg 8194.47 Some(false) None], [/home/chad/work/apma507_scans/ou
                                                  //| t1-34.jpg 7655.92 Some(false) None], [/home/chad/work/apma507_scans/out44-2
                                                  //| 7.jpg 7581.85 Some(false) None], [/home/chad/work/apma507_scans/out44-37.jp
                                                  //| g 9401.1 Some(false) None], [/home/chad/work/apma507_scans/out44-4.jpg 4195
                                                  //| .3 Some(true) None])
	val objs2 = objs_skip ++ explicit_train_objs
                                                  //> objs2  : List[imageData] = List([/home/chad/work/apma507_scans/out1-25.jpg 
                                                  //| 11239.1 None None], [/home/chad/work/apma507_scans/out1-17.jpg 7549.48 None
                                                  //|  None], [/home/chad/work/apma507_scans/out44-10.jpg 3695.97 None None], [/h
                                                  //| ome/chad/work/apma507_scans/out1-9.jpg 8369.6 None None], [/home/chad/work/
                                                  //| apma507_scans/out1-38.jpg 12122.6 None None], [/home/chad/work/apma507_scan
                                                  //| s/out44-15.jpg 8194.47 Some(false) None], [/home/chad/work/apma507_scans/ou
                                                  //| t1-34.jpg 7655.92 Some(false) None], [/home/chad/work/apma507_scans/out44-2
                                                  //| 7.jpg 7581.85 Some(false) None], [/home/chad/work/apma507_scans/out44-37.jp
                                                  //| g 9401.1 Some(false) None], [/home/chad/work/apma507_scans/out44-4.jpg 4195
                                                  //| .3 Some(true) None])
	val train_data = objs2.filter(x => x.isBlankExplicit.isDefined).map(x => (x.stdDev, x.isBlankExplicit.getOrElse(false)))
                                                  //> train_data  : List[(Double, Boolean)] = List((8194.47,false), (7655.92,fals
                                                  //| e), (7581.85,false), (9401.1,false), (4195.3,true))
  val all_stdevs = objs2.map(x => x.stdDev)       //> all_stdevs  : List[Double] = List(11239.1, 7549.48, 3695.97, 8369.6, 12122.
                                                  //| 6, 8194.47, 7655.92, 7581.85, 9401.1, 4195.3)
  val probs = convertScans.getProbOfBlank(train_data, all_stdevs)
                                                  //> probs  : List[Double] = List(4.444759141710934E-22, 3.9922458404922336E-7, 
                                                  //| 0.999999999395778, 1.8941655610280243E-10, 1.1672958085445001E-25, 9.709312
                                                  //| 248789978E-10, 1.478546967100844E-7, 2.951396162486022E-7, 1.25006653927756
                                                  //| 01E-14, 0.9999999361895863)
  val obj3 = objs2.zip(probs).map({case (x, y) => new imageData(x.filename, x.stdDev, x.isBlankExplicit, Some(y))})
                                                  //> obj3  : List[imageData] = List([/home/chad/work/apma507_scans/out1-25.jpg 1
                                                  //| 1239.1 None Some(4.444759141710934E-22)], [/home/chad/work/apma507_scans/ou
                                                  //| t1-17.jpg 7549.48 None Some(3.9922458404922336E-7)], [/home/chad/work/apma5
                                                  //| 07_scans/out44-10.jpg 3695.97 None Some(0.999999999395778)], [/home/chad/wo
                                                  //| rk/apma507_scans/out1-9.jpg 8369.6 None Some(1.8941655610280243E-10)], [/ho
                                                  //| me/chad/work/apma507_scans/out1-38.jpg 12122.6 None Some(1.1672958085445001
                                                  //| E-25)], [/home/chad/work/apma507_scans/out44-15.jpg 8194.47 Some(false) Som
                                                  //| e(9.709312248789978E-10)], [/home/chad/work/apma507_scans/out1-34.jpg 7655.
                                                  //| 92 Some(false) Some(1.478546967100844E-7)], [/home/chad/work/apma507_scans/
                                                  //| out44-27.jpg 7581.85 Some(false) Some(2.951396162486022E-7)], [/home/chad/w
                                                  //| ork/apma507_scans/out44-37.jpg 9401.1 Some(false) Some(1.2500665392775601E-
                                                  //| 14)], [/home/chad/work/apma507_scans/out44-4.jpg 4195.3 Some(true) Some(0.9
                                                  //| 999999361895863)])
	val objs4blankmiddle = obj3.filter(x => x.probBlank.getOrElse(.5) >= explicitTrainProbLower && x.probBlank.getOrElse(.5) <= 1-explicitTrainProbLower)
                                                  //> objs4blankmiddle  : List[imageData] = List()
  val isblankmiddle = objs4blankmiddle.map(x => convertScans.isImageBlankExplicit(x.filename))
                                                  //> isblankmiddle  : List[Boolean] = List()
	val objs5_blankmiddle = objs4blankmiddle.zip(isblankmiddle).map({case (x, y) => new imageData(x.filename, x.stdDev, Some(y), x.probBlank)})
                                                  //> objs5_blankmiddle  : List[imageData] = List()
	val objs5 = objs5_blankmiddle ++ obj3.filter(x => !(x.probBlank.getOrElse(.5) >= explicitTrainProbLower && x.probBlank.getOrElse(.5) <= 1-explicitTrainProbLower))
                                                  //> objs5  : List[imageData] = List([/home/chad/work/apma507_scans/out1-25.jpg 
                                                  //| 11239.1 None Some(4.444759141710934E-22)], [/home/chad/work/apma507_scans/o
                                                  //| ut1-17.jpg 7549.48 None Some(3.9922458404922336E-7)], [/home/chad/work/apma
                                                  //| 507_scans/out44-10.jpg 3695.97 None Some(0.999999999395778)], [/home/chad/w
                                                  //| ork/apma507_scans/out1-9.jpg 8369.6 None Some(1.8941655610280243E-10)], [/h
                                                  //| ome/chad/work/apma507_scans/out1-38.jpg 12122.6 None Some(1.167295808544500
                                                  //| 1E-25)], [/home/chad/work/apma507_scans/out44-15.jpg 8194.47 Some(false) So
                                                  //| me(9.709312248789978E-10)], [/home/chad/work/apma507_scans/out1-34.jpg 7655
                                                  //| .92 Some(false) Some(1.478546967100844E-7)], [/home/chad/work/apma507_scans
                                                  //| /out44-27.jpg 7581.85 Some(false) Some(2.951396162486022E-7)], [/home/chad/
                                                  //| work/apma507_scans/out44-37.jpg 9401.1 Some(false) Some(1.2500665392775601E
                                                  //| -14)], [/home/chad/work/apma507_scans/out44-4.jpg 4195.3 Some(true) Some(0.
                                                  //| 9999999361895863)])|
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
	
	def getImageFilenamesInDirectory(dir : String) : Array[String] =
		return new File(dir).listFiles.map(x => x.getPath).filter(x => x.endsWith(".jpg"))
		
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
}

class imageData(val filename: String,
	val stdDev: Double,
	val isBlankExplicit : Option[Boolean] = None,
	val probBlank : Option[Double]= None) {
	override def toString(): String =
		return "[" + filename + " " + stdDev.toString + " " + isBlankExplicit.toString + " " + probBlank.toString + "]"
}