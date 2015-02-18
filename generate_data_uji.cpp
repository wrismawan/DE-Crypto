#include <iostream>
#include <fstream>
#include <string>
using namespace std;
int main() {
    int A, B, CC, i;
    ifstream ifs("data/mentah/data1.txt");
    char plain[10000];
    string S;
    char plaintext[10000];
    i=0;
    
    while(getline(ifs,S)) {
        CC=S.length();
        for(int j=0;j<CC;j++){
            plain[i]=S[j];i++;
        }
    }
    
    int newI=0;
    for (int i=0;i<CC;i++){
        if (isalpha(plain[i])){
            plaintext[newI] = plain[i];
            newI++;
        }
    }
    
    cout<<plaintext<<endl;
    int C = strlen(plaintext);
    int D;
    
    cout << "Masukkan panjang kunci : " <<endl;
    cin >> D;
    
    int CA=D-(C%D);
    for(int i=0;i<CA;i++)
        plaintext[C+i]='a' + rand()%26;
    
    C=C+CA;

    int key[D];
    cout << "Masukkan kunci : " << endl;
    for (int i=0; i<D; i++){
        cin >> key[i];
        if (key[i]>D){
            cout<<"Masukkan kunci yang lain"<<endl;cin >> key[i];
        }

        for(int j=0;j<i;j++){
            if(key[i]==key[j]){
                cout<<"Masukkan kunci yang lain"<<endl;cin >> key[i];
            }
        }
    }

    cout<<"====================================================="<<endl;
    cout<<"SUMMARY"<<endl;
    cout<<"====================================================="<<endl;
    cout<<"PLAINTEXT : "<<endl;
    cout<<plain<<endl;
    cout<<"PANJANG PLAINTEXT : "<<newI<<endl;
    cout<<"PANJANG KUNCI : "<<D<<endl;
    cout<<"KUNCI : ";
    for(int i=0;i<D;i++)
        cout<<key[i]<<" ";
    cout<<endl;
    cout<<"CIPHERTEXT : "<<endl;
    for (int i=0; i<C; i++){
        A = i%D;
        B = i/D;
        cout<<plaintext[B*D+key[A]-1];
    }
    cout<<endl;
    return 0;
}
