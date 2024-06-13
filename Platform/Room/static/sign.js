let django_url = my_url
let token = csrftoken

async function signFile(id) { 
    try{
      let formData = new FormData();
      formData.append('id', id)
      // formData.append('doc', file.files[0]);

      let data = await fetch(django_url,{
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrftoken,
        }})
      .then(response => response.json());

      const mess = data.cid

      if (!window.ethereum) {
        alert('Metamask not installed')
        return null;
      }

      const provider = new ethers.providers.Web3Provider(window.ethereum)
      await provider.send("eth_requestAccounts", []);
      const signer = provider.getSigner()
      if(signer == null) return;
      const signature = await signer.signMessage(mess);
      
      const form = document.getElementById('submit form');
      const t = document.createElement('input');
      t.setAttribute('type', 'text');
      t.setAttribute('name', 'signature');
      t.setAttribute('value', signature);
      form.appendChild(t)

      form.submit();

      t.remove();
    } catch (error) {
      console.error(error);
    }
}