import com.android.apksig.ApkSigner;
import java.io.*; import java.security.*; import java.security.cert.X509Certificate; import java.util.*;
public class Sign { public static void main(String[] a) throws Exception {
  KeyStore ks=KeyStore.getInstance("PKCS12"); try(InputStream in=new FileInputStream(a[0])){ks.load(in,a[1].toCharArray());}
  PrivateKey k=(PrivateKey)ks.getKey("key",a[1].toCharArray()); X509Certificate c=(X509Certificate)ks.getCertificate("key");
  ApkSigner.SignerConfig sc=new ApkSigner.SignerConfig.Builder("key",k,Collections.singletonList(c)).build();
  new ApkSigner.Builder(Collections.singletonList(sc)).setInputApk(new File(a[2])).setOutputApk(new File(a[3])).setV1SigningEnabled(false).setV2SigningEnabled(true).setMinSdkVersion(24).build().sign();
  com.android.apksig.ApkVerifier.Result r=new com.android.apksig.ApkVerifier.Builder(new File(a[3])).build().verify();
  System.out.println("verified="+r.isVerified()+" v1="+r.isVerifiedUsingV1Scheme()+" v2="+r.isVerifiedUsingV2Scheme()+" errors="+r.getErrors());
}}
