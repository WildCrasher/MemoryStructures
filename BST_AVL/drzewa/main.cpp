#include <iostream>
#include<cmath>

using namespace std;

int levelGlobal = 0;
struct AVL
{
    AVL *parent, *left, *right;
    int key;
};

/*void create_AVL(AVL * &root,int tab[],int left,int right,AVL *parent)
{
    int n;
    n=(right+left)/2;
    root->key=tab[n];
    root->left=new AVL;
    root->right=new AVL;
    root->parent=parent;
//    cout<<n<<endl;

    if(right-left>0)
    {
        if(right-left==1)
        {
            create_AVL(root->right,tab,n+1,right,root);
        }
        else if((right-left)%2==0)
        {
            create_AVL(root->left,tab,n-(right-n),n-1,root);
            create_AVL(root->right,tab,n+1,right,root);
        }
        else if((right-left)%2==1)
        {
            create_AVL(root->left,tab,n-(right-n)+1,n-1,root);
            create_AVL(root->right,tab,n+1,right,root);
        }

    }



}*/
void insert_BST(AVL * &root,int key)
{
    AVL *n,*parent;

    n=new AVL;

    n->left=n->right=NULL;
    n->key=key;

    parent=root;
    if(!parent)
    {
      //  cout<<"dupa"<<endl;
        root=n;
    }
    else
    while(true)
        if(key<parent->key)
        {
            if(!parent->left)
            {
                parent->left=n;
                break;
            }
            else
                parent=parent->left;
        }
        else
        {
            if(!parent->right)
            {
                parent->right=n;
                break;
            }
            else
                parent=parent->right;
        }
    n->parent=parent;

}

void create_BST(AVL * &root,int tab[],int n)
{
    for(int i=0;i<n;i++)
    {
        insert_BST(root,tab[i]);
    }
}
void show_tree(AVL *root, char leftOrRight = 'P')
{
    if(root) {
    	levelGlobal++;
    	cout<<root->key<<leftOrRight<<"-level:"<<levelGlobal<<endl;
	}
    if(root->left) {
    	show_tree(root->left, 'L');	
	}
    if(root->right) {
    	show_tree(root->right, 'R');
	}
}
void create_AVL(AVL * &root,int tab[],int left,int right)
{
       int n;
    n=(right+left)/2;
    insert_BST(root,tab[n]);
//    cout<<n<<endl;

    if(right-left>0)
    {
        if(right-left==1)
        {
            create_AVL(root,tab,n+1,right);
        }
        else if((right-left)%2==0)
        {
            create_AVL(root,tab,n-(right-n),n-1);
            create_AVL(root,tab,n+1,right);
        }
        else if((right-left)%2==1)
        {
            create_AVL(root,tab,n-(right-n)+1,n-1);
            create_AVL(root,tab,n+1,right);
        }

    }
}
int min(AVL *root)
{
    while(root->left)
        root=root->left;
    return root->key;
}
void show_tree_ros(AVL *root)
{
    if(root->left)
    show_tree_ros(root->left);
    cout<<root->key<<endl;
    if(root->right)
    show_tree_ros(root->right);
}
int get_root(AVL *root)
{
    if(root)
    return root->key;
    else return 0;
}
void delete_tree(AVL * &root)
{
    if(root->left)
        delete_tree(root->left);

    if(root->right)
        delete_tree(root->right);
    delete root;
    root=NULL;
}
void rotacja_prawa(AVL * &root,AVL *A)
{
    AVL *B=A->left, *p=A->parent;
    A->left=B->right;
    if(A->left)A->left->parent=A;
    B->right=A;
    B->parent=p;
    A->parent=B;
    if(p)
    {
        if(p->left==A)p->left=B; else p->right=B;
    }
    else root=B;
}
void rotacja_lewa(AVL * &root,AVL *A)
{
    AVL *B=A->right, *p=A->parent;
    A->right=B->left;
    if(A->right)A->right->parent=A;
    B->left=A;
    B->parent=p;
    A->parent=B;
    if(p)
    {
        if(p->left==A)p->left=B; else p->right=B;
    }
    else root=B;
}
int DSW_1(AVL * &root)
{
    int n=0;
    AVL *tmp=root;
    while(tmp)
    {
        if(tmp->left)
        {
            rotacja_prawa(root,tmp);
            tmp=tmp->parent;
        }

        else
        {
            tmp=tmp->right;
            n++;
        }

    }
    return n;
}
void DSW_2(AVL * &root,int n)
{

    int m = pow(2, (int)log2(n + 1)) - 1;
    //cout<<m<<endl;
    AVL *tmp = root;
    for(int i=0;i<n-m;i++)
    {
             rotacja_lewa(root,tmp);
            tmp=tmp->parent->right;

    }
    tmp=root;
    while(m>1)
    {
        m/=2;
        tmp=root;
        for(int i=0;i<m;i++)
        {
            if(tmp)
            {
                rotacja_lewa(root,tmp);
                tmp=tmp->parent->right;
            }

        }
    }
}
void DSW(AVL * &root)
{
    int n=DSW_1(root);
    DSW_2(root,n);
}
void usun(AVL * &root)
{
    cout<<"Ile liczb chcesz usunac?"<<endl;
    int ile;
    cin>>ile;
    int n=DSW_1(root);
    int liczba;
    AVL *tmp=root;
    for(int i=0;i<ile;i++)
    {
        cout<<"Podaj kolejna liczbe"<<endl;
        cin>>liczba;
        while(tmp->right && tmp->key!=liczba)
        {
            tmp=tmp->right;
        }
        if(tmp->parent)
        {
            if(tmp->right)
            {
                tmp->parent->right=tmp->right;
                tmp->right->parent=tmp->parent;
                delete tmp;
                tmp=NULL;
            }
            else
            {
                tmp->parent->right=NULL;
                delete tmp;
                tmp=NULL;
            }

        }
        else
        {
            tmp->right->parent=NULL;
            root=tmp->right;
            delete tmp;
            tmp=NULL;
        }
        tmp=root;
    }
    n-=ile;
    DSW_2(root,n);
    cout<<"Usunieto podane wezly\n";
}

void create_BST_during_removal(AVL * &root,int tab[],int n, int key, int k)
{
    int j;
    for(int i=0;i<n-k;i++)
    {
        if (tab[i]==key)
        {
            j=i;
            while(j <= n-2)
            {
                swap(tab[j],tab[j+1]);
                j++;
            }
        }
        insert_BST(root,tab[i]);
    }
}

void remove_node_BST (AVL * &root, int tab[], int n)
{
    int key,ile;
    cout<<"Podaj ile liczb chcesz usunac\n";
    cin>>ile;
    for(int i=0;i<ile;i++)
    {
        cout<<"Podaj kolejna liczbe"<<endl;
        cin>>key;
        delete_tree(root);
        create_BST_during_removal(root,tab,n,key,i+1);
    }
    cout<<"Usunieto podane wezly"<<endl;
}

int height(AVL* root) {
	if (root == NULL)
        return -1;
   else
        return max(height(root->left), height(root->right)) + 1;	
}

void printGivenLevel(AVL* root, int level) 
{ 
    if (root == NULL) 
        return; 
    if (level == 1) 
        printf("%d ", root->key); 
    else if (level > 1) 
    { 
        printGivenLevel(root->left, level-1); 
        printGivenLevel(root->right, level-1); 
    } 
}

void printLevelOrder(AVL* root) 
{ 
    int h = height(root);
    cout<<"height:"<<h<<endl;
    int i; 
    for (i=1; i<=h + 1; i++) 
    { 
        printGivenLevel(root, i); 
        printf("\n"); 
    } 
}



int main()
{
    const int n=7;
    int tab[n]={10,5,15,3,7,17,14};
    AVL *root=NULL;
    AVL *rootBST=NULL;
    create_AVL(root,tab,0,n-1);
    create_BST(rootBST,tab,n);
    printLevelOrder(rootBST);
    cout<<endl;
    printLevelOrder(root);
    show_tree(rootBST);
    levelGlobal = 0;
    cout<<endl;
    DSW(root);
    printLevelOrder(root);
//    show_tree(root);
//    levelGlobal = 0;
//    show_tree_ros(rootBST); cout<<endl;
//    cout<<"min AVL="<<min(root)<<endl;
//    cout<<"min BST="<<min(rootBST)<<endl;
//    remove_node_BST(rootBST,tab,n);
//    usun(root);
//    show_tree_ros(root); cout<<endl;
//    show_tree_ros(rootBST); cout<<endl;
//    cout<<get_root(root)<<endl;
//    cout<<get_root(rootBST)<<endl;
//    delete_tree(root);
//    delete_tree(rootBST);
    //show_tree(rootBST);
    return 0;
}
