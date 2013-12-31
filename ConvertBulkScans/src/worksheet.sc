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
	val explicitTrainNumber = 2;
	//val filenames = convertScans.getImageFilenamesInDirectory("/home/chad/work/apma507_scans").take(3)
	//val stdevs = convertScans.getImageStandardDeviations(filenames.toList)
	//val objs = filenames.zip(stdevs).map({case (x, y) => new imageData(x, y)})
  //val num_explicit_train = min(explicitTrainNumber, objs.length)
  //val objs_shuffle = Random.shuffle(objs.toList)
  //val objs_train = objs_shuffle.take(num_explicit_train)
  //val objs_skip = objs_shuffle.drop(num_explicit_train)
	//val explicit_blank = objs_train.map(x => convertScans.isImageBlankExplicit(x.filename))
	//val explicit_train_objs = objs_train.zip(explicit_blank).map({case (x, y) => new imageData(x.filename, x.stdDev, Some(y))})
	//val objs2 = objs_skip ++ explicit_train_objs

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
				
	  var data = new weka.core.Instances("myRelation", atts, 0);
		for (i <- 0 until train_data.length) {
			match
			val booldbl = train_data(i)
			train_data(i).
		}
		ignore = data.add(new weka.core.DenseInstance(1.0, Array(5.0, 0)));
		ignore = data.add(new weka.core.DenseInstance(1.0, Array(4.0, 1.0)));
		ignore = data.add(new weka.core.DenseInstance(1.0, Array(0.9, 1.0)));
		data.setClassIndex(data.numAttributes() - 1);
	  
		var lr = new weka.classifiers.functions.Logistic()
		lr.buildClassifier(data);
	  var data2 = new weka.core.Instances("myRelation", atts, 0);
	  ignore = data2.add(new weka.core.DenseInstance(1.0, Array(4.5, 0.0)));
	  data2.setClassIndex(data2.numAttributes() - 1);
	  var yyy = lr.distributionForInstance(data2.get(0))(1);
		return 1.0 :: Nil
	}
}

class imageData(val filename: String,
	val stdDev: Double,
	val isBlankExplicit : Option[Boolean] = None,
	val probBlank : Option[Double]= None) {
	override def toString(): String =
		return "[" + filename + " " + stdDev.toString + " " + isBlankExplicit.toString + " " + probBlank.toString + "]"
}